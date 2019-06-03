import re
import hashlib
import warnings
import logging
from datetime import datetime, timedelta

import feedparser
import requests
import rapidjson as json
from dal import autocomplete
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.views.decorators.http import require_POST

from articles.models import Newspaper, Subscription, SubscriptionToAuthor
from articles.period import parse_periodicity
from credits.utils import (get_user_credits, pay_author_subscription,
                           pay_newspaper_subscription)
from sources.models import Channel
from sources.management.commands.importrss import import_feed_entry, get_entry_publish_date
from users.models import User
from utils.decorators import ajax_login_required
from utils.json import JsonResponse


RE_NEWSPAPER = re.compile(r'https?://kairly.com/([^/]+)/([^/]+)/rss$')


def is_rss(header):
    just_type = header.split(';')[0]
    try:
        second_part = just_type.split('/')[1]
    except IndexError:
        second_part = just_type

    # allow also html, lot of feeds returns invalid text/html
    return second_part in ('rss+xml', 'rss', 'xml', 'atom+xml', 'html')


@ajax_login_required
@require_POST
@transaction.atomic
def import_rss(request):
    payload = json.loads(request.body.decode('utf-8'))
    url = payload['url']

    m = RE_NEWSPAPER.match(url)
    if m:
        # special casefeed item is kairly newspaper
        try:
            newspaper = Newspaper.objects.get(slug=m[2], editor__username=m[1])
        except Newspaper.DoesNotExist:
            return JsonResponse({'error': 'Unknown newspaper'})

        return JsonResponse({
            'type': 'newspaper',
            'fullName': newspaper.full_name
        })

    def response_for_channel(channel):
        if channel.newspaper:
            return JsonResponse({
                'type': 'newspaper',
                'fullName': channel.newspaper.full_name
            })
        else:
            return JsonResponse({
                'type': 'author',
                'username': channel.author.username
            })

    try:
        channel = Channel.objects.get(Q(rss=url) | Q(alternaterss__rss=url), enabled=True)
        return response_for_channel(channel)
    except Channel.DoesNotExist:
        pass

    try:
        headers = {'User-Agent': settings.DEFAULT_USER_AGENT}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            resp = requests.get(url, headers=headers, allow_redirects=True, timeout=1, verify=False)
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'Request timed out.'})
    except IOError as e:
        return JsonResponse({'error': str(e)})

    if not resp.ok:
        return JsonResponse({'error': f"Feed request returned {resp.status_code}"})

    content_type = resp.headers['Content-Type']

    if not is_rss(content_type):
        return JsonResponse({'error': f"Not feed content type, got {content_type}"})

    if url != resp.url:
        # redirect happend, try to reload channel with new url
        url = resp.url
        try:
            channel = Channel.objects.get(rss=url)
            return response_for_channel(channel)
        except Channel.DoesNotExist:
            pass

    rss = feedparser.parse(resp.content)

    if hasattr(rss.feed, 'html'):
        return JsonResponse({'error': f"Resource is not valid feed"})

    if not rss.feed:
        if rss.bozo:
            return JsonResponse({'error': str(getattr(rss, 'bozo_exception', ''))})
        else:
            return JsonResponse({'error': f"Resource is not valid feed"})

    uniq_id = hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]
    title = rss.feed.title or url.replace('https://', '').replace('http://')
    author = User.objects.create(
        username=f"feed-{uniq_id}",
        name=title,
        email='',
        kind=User.FEED,
        is_active=False,
        medium='',
        bio=rss.feed.subtitle + '\n' + url if rss.feed.subtitle else url
    )

    channel = Channel.objects.create(
        name=title,
        provider=uniq_id,
        rss=url,
        import_links=True,
        parser='*',
        directives='',
        author=author,
    )

    date_limit = timezone_now() - timedelta(days=1)
    count_limit = 3
    for entry in rss.entries:
        published = get_entry_publish_date(entry)
        if published > date_limit:
            try:
                import_feed_entry(channel, entry)
                count_limit -= 1
                if count_limit == 0:
                    break
            except requests.exceptions.SSLError as e:
                logging.warning(str(e))
                # do not try other links
                # to not block web worker for long time
                break
            except IOError as e:
                logging.warning(str(e))

    return JsonResponse({
        'type': 'author',
        'username': author.username
    })


@ajax_login_required
@require_POST
@transaction.atomic
def subscribe_rss(request):
    now = datetime.now(request.user.tzinfo)
    payload = json.loads(request.body.decode('utf-8'))
    newspaper_items = payload['newspapers']
    author_items = payload['authors']

    credits = get_user_credits(request.user.id)

    if newspaper_items:
        bulk = []

        query = None
        for n in newspaper_items:
            username, slug = n['fullName'].split('/', maxsplit=1)
            q = Q(editor__username=username, slug=slug)
            query = q if query is None else query | q

        newspapers = list(Newspaper.objects.filter(query).select_related('editor'))
        already_subscribed = set(
            s.newspaper_id for s in
            Subscription.objects.filter(Q(valid_to__gt=now) | Q(renewal=True), user=request.user, newspaper__in=newspapers))
        if already_subscribed:
            newspapers = [n for n in newspapers if n.id not in already_subscribed]

        for newspaper in newspapers:
            has_credits = credits >= newspaper.price

            subscription = Subscription(
                user=request.user,
                newspaper=newspaper
            )

            if has_credits:
                subscription.suspended = False
                subscription.valid_from = now
                subscription.valid_to = now + relativedelta(months=1)
            else:
                subscription.suspended = True
                subscription.valid_from = now - relativedelta(months=1)
                subscription.valid_to = now

            bulk.append(subscription)

            if has_credits:
                credits -= newspaper.price
                pay_newspaper_subscription(subscription)

        if bulk:
            Subscription.objects.bulk_create(bulk)

    if author_items:
        bulk = []
        ids = [item['username'] for item in author_items]
        periodicities = {item['username']: parse_periodicity(item['periodicity']) for item in author_items}

        authors = list(User.objects.filter(username__in=ids))
        already_subscribed = set(
            s.author_id for s in
            SubscriptionToAuthor.objects.filter(Q(valid_to__gt=now) | Q(renewal=True), user=request.user, author__in=authors))
        if already_subscribed:
            authors = [a for a in authors if a.id not in already_subscribed]

        for author in authors:
            has_credits = credits >= author.price

            subscription = SubscriptionToAuthor(
                user=request.user,
                author=author
            )

            if has_credits:
                subscription.suspended = False
                subscription.valid_from = now
                subscription.valid_to = now + relativedelta(months=1)
            else:
                subscription.suspended = True
                subscription.valid_from = now - relativedelta(months=1)
                subscription.valid_to = now

            subscription.set_periodicity(periodicities[author.username])
            bulk.append(subscription)

            if has_credits:
                credits -= author.price
                pay_author_subscription(subscription)

        if bulk:
            SubscriptionToAuthor.objects.bulk_create(bulk)

    return JsonResponse({
        'credits': str(credits),
    })


class ChannelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return Channel.objects.none()

        qs = Channel.objects.filter(enabled=True)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(rss__icontains=self.q))

        return qs

    def get_result_label(self, item):
        return f"{item.name} - {item.rss}"
