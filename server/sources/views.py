import re
import hashlib
from datetime import timedelta

import feedparser
import requests
import rapidjson as json
from django.db import transaction
from django.conf import settings
from django.utils.timezone import now as timezone_now
from django.views.decorators.http import require_POST

from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from articles.models import Newspaper
from sources.models import Channel
from sources.management.commands.importrss import import_feed_entry, get_entry_publish_date
from users.models import User


RE_NEWSPAPER = re.compile(r'https?://kairly.com/([^/]+)/([^/]+)/rss$')


def is_rss(header):
    just_type = header.split(';')[0]
    try:
        second_part = just_type.split('/')[1]
    except IndexError:
        second_part = just_type

    return second_part in ('rss+xml', 'rss', 'xml', 'atom+xml')


@ajax_login_required
@require_POST
@transaction.atomic
def import_rss(request):
    payload = json.loads(request.body.decode('utf-8'))

    source = payload['source']
    url = source['xmlUrl']
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

    try:
        headers = {'User-Agent': settings.DEFAULT_USER_AGENT}
        resp = requests.get(url, headers=headers, allow_redirects=True, timeout=3)
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'Request timed out.'})
    except IOError as e:
        return JsonResponse({'error': str(e)})

    if not resp.ok:
        return JsonResponse({'error': f"Feed request returned {resp.status_code}"})

    url = resp.url
    content_type = resp.headers['Content-Type']

    if not is_rss(content_type):
        return JsonResponse({'error': f"Not feed content type, got {content_type}"})

    try:
        channel = Channel.objects.get(rss=url)
        if channel.newspaper:
            return JsonResponse({
                'type': 'newspaper',
                'fullName': channel.newspaper.full_name
            })
        else:
            return JsonResponse({
                'type': 'author',
                'id': channel.author.username
            })
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

        channel = Channel.objects.create(
            name=source['title'],
            provider=uniq_id,
            rss=url,
            import_links=True,
            parser='*',
            directives='',
            author=author,
        )

        rss = feedparser.parse(resp.content)
        date_limit = timezone_now() - timedelta(days=1)
        count_limit = 3
        for entry in rss.entries:
            published = get_entry_publish_date(entry)
            if published > date_limit:
                import_feed_entry(channel, entry)
                count_limit -= 1
                if count_limit == 0:
                    break

        return JsonResponse({
            'type': 'author',
            'id': author.username
        })
