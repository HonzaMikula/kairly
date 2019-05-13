import re
import hashlib
from datetime import datetime
from decimal import Decimal

import requests
import rapidjson as json
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from dateutil.relativedelta import relativedelta

from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from articles.models import Newspaper, Subscription, SubscriptionToAuthor
from articles.period import parse_periodicity
from credits.utils import pay_newspaper_subscription, pay_author_subscription, get_user_credits
from sources.models import Channel
from users.models import User


RE_NEWSPAPER = re.compile(r'https?://kairly.com/([^/]+)/([^/]+)/rss$')


@ajax_login_required
@require_POST
@transaction.atomic
def import_rss(request):
    payload = json.loads(request.body.decode('utf-8'))
    now = datetime.now(request.user.tzinfo)
    newspaper_subscriptions = []
    author_subscriptions = []
    channels = []

    # sid = transaction.savepoint()

    credits = get_user_credits(request.user.id)

    def subscribe_newspaper(newspaper):
        nonlocal credits
        if credits > newspaper.price or newspaper.price == 0:
            subscription = Subscription(
                user=request.user,
                newspaper=newspaper,
                valid_from=now,
                valid_to=now + relativedelta(months=1),
                donation=Decimal(0),
            )
            pay_newspaper_subscription(subscription)
        else:
            credits -= newspaper.price
            subscription = Subscription(
                user=request.user,
                newspaper=newspaper,
                valid_from=now - relativedelta(months=1),
                valid_to=now,
                donation=Decimal(0),
                suspended=True
            )
        newspaper_subscriptions.append(subscription)

    def subscribe_author(author, periodicity):
        nonlocal credits
        if credits > author.price or author.price == 0:
            subscription = SubscriptionToAuthor(
                user=request.user,
                author=author,
                valid_from=now,
                valid_to=now + relativedelta(months=1),
                donation=Decimal(0),
            )
            pay_author_subscription(subscription)
        else:
            credits -= author.price
            subscription = SubscriptionToAuthor(
                user=request.user,
                author=author,
                valid_from=now - relativedelta(months=1),
                valid_to=now,
                donation=Decimal(0),
                suspended=True
            )
        subscription.set_periodicity(periodicity)
        author_subscriptions.append(subscription)

    for source in payload['sources']:
        url = source['xmlUrl']
        m = RE_NEWSPAPER.match(url)
        if m:
            # special casefeed item is kairly newspaper
            try:
                newspaper = Newspaper.objects.get(slug=m[2], editor__username=m[1])
            except Newspaper.DoesNotExist:
                print(f"Unknown newspaper {url}")
                continue

            subscribe_newspaper(newspaper)
            continue

        # feed item is regular url
        try:
            resp = requests.head(url, allow_redirects=True, timeout=5)
        except requests.exceptions.Timeout:
            print(f"{url} time out")
            continue

        try:
            periodicity = parse_periodicity(source['periodicity'])
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        url = resp.url
        content_type = resp.headers['Content-Type'].split(';')[0]

        if content_type.split('/')[1] not in ('rss+xml', 'xml', 'atom+xml'):
            print(f"Unknown content type {content_type} for {url}")
            continue

        try:
            channel = Channel.objects.get(rss=url)
            if channel.newspaper:
                subscribe_newspaper(channel.newspaper)
            else:
                subscribe_author(channel.author, periodicity)
        except Channel.DoesNotExist:
            uniq_id = hashlib.sha224(url.encode('utf-8')).hexdigest()[:12]
            author = User.objects.create(
                username=f"feed-{uniq_id}",
                name=source['title'],
                email='',
                kind=User.FEED,
                medium='',
                bio=url
            )

            channels.append(Channel(
                name=source['title'],
                provider=uniq_id,
                rss=url,
                import_links=True,
                parser='*',
                directives='',
                author=author,
            ))

            subscription = SubscriptionToAuthor(
                user=request.user,
                author=author,
                valid_from=now,
                valid_to=now + relativedelta(months=1),
                donation=Decimal(0),
            )
            subscription.set_periodicity(periodicity)
            author_subscriptions.append(subscription)

    if newspaper_subscriptions:
        Subscription.objects.bulk_create(newspaper_subscriptions)
    if author_subscriptions:
        SubscriptionToAuthor.objects.bulk_create(author_subscriptions)
    if channels:
        Channel.objects.bulk_create(channels)

    # just debug code
    # transaction.savepoint_rollback(sid)

    return JsonResponse({
        'credits': str(credits)
    })
