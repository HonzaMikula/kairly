import json
import time
import dateutil.parser
from operator import itemgetter
from itertools import chain
from datetime import datetime, timedelta

from more_itertools import peekable

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from utils.decorators import ajax_login_required
from .models import Issue, Post, Subscription, SubscriptionToAuthor


DAY_START_HOUR = 6


@ajax_login_required
def timeline(request):
    # Group author issues by period defined by client local zone
    # It means that timeline for same user may differ when user is in different
    # timezone.
    tzinfo = request.user.tzinfo
    now = datetime.now(tzinfo)

    date_str = request.GET.get('date')
    if date_str:
        d = dateutil.parser.parse(date_str).date()
    else:
        d = now.date()
        if now.hour < DAY_START_HOUR:
            d -= timedelta(days=1)

    # use now.replace to preserve tzinfo
    start_dt = now.replace(year=d.year, month=d.month, day=d.day,
                           hour=0, minute=0, second=0, microsecond=0)
    end_dt = start_dt + timedelta(days=1)

    if start_dt > now:
        return HttpResponseBadRequest("Invalid date.")

    recent_day = now < end_dt + timedelta(hours=DAY_START_HOUR)

    links = {
        'prev': str(d - timedelta(days=1))
    }
    if not recent_day:
        links['next'] = str(d + timedelta(days=1))

    if recent_day and now < end_dt:
        cache_valid_to = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        cache_valid_to = int(cache_valid_to.timestamp())
        end_dt = now
    else:
        cache_valid_to = None

    newspaper_issues, newspaper_subscription_exists = get_newspaper_issues(
        request, now, tzinfo, start_dt, end_dt, cache_valid_to)

    author_issues, author_subscription_exists = get_author_issues(
        request, now, tzinfo, start_dt, end_dt, cache_valid_to)

    if not newspaper_subscription_exists and not author_subscription_exists:
        # no subscription exists
        return HttpResponse(status=204)

    issues = list(sorted(
        chain(newspaper_issues, author_issues),
        key=itemgetter('time'), reverse=True))

    return JsonResponse({
        'date': str(d),
        'issues': issues,
        'links': links,
        'validTo': cache_valid_to,
    })


def get_newspaper_issues(request, now, tzinfo, start_dt, end_dt, cache_valid_to):
    subscriptions = Subscription.objects.filter(
        user=request.user,
        renewal=True,
        valid_from__lte=now,
        valid_to__gt=now
    ).select_related('newspaper', 'newspaper__editor')

    issues = []
    subscription_exists = False
    for sub in subscriptions:
        subscription_exists = True

        issues.extend(
            get_newspaper_subscription_issues(sub, tzinfo, start_dt, end_dt, cache_valid_to)
        )
    return issues, subscription_exists


def get_newspaper_subscription_issues(sub, tzinfo, start_dt, end_dt, cache_valid_to):
    newspaper_name = "{}/{}".format(sub.newspaper.editor.username, sub.newspaper.slug)
    cache_key = "newspaper_issues_{}_{}-{}".format(
        newspaper_name,
        int(start_dt.timestamp()),
        int(end_dt.timestamp() if cache_valid_to is None else cache_valid_to)
    )

    cached_issues = cache.get(cache_key)
    if cached_issues:
        return json.loads(cached_issues)

    query = Issue.objects.filter(
        published__gte=start_dt, published__lt=end_dt,
        newspaper=sub.newspaper
    )

    issues = []
    for issue in query:
        issues.append(issue.to_json(
            newspaper=sub.newspaper,
            tzinfo=tzinfo))

    if cache_valid_to is None:
        timeout = None
    else:
        timeout = max(0, cache_valid_to - int(time.time()))
    cache.set(cache_key, json.dumps(issues), timeout)
    return issues


def get_author_issues(request, now, tzinfo, start_dt, end_dt, cache_valid_to):
    subscriptions = SubscriptionToAuthor.objects.filter(
        user=request.user,
        renewal=True,
        valid_from__lte=now,
        valid_to__gt=now
    ).select_related('author')

    issues = []
    subscription_exists = False

    for sub in subscriptions:
        subscription_exists = True
        issues.extend(
            get_author_subscription_issues(sub, tzinfo, start_dt, end_dt, cache_valid_to)
        )

    return issues, subscription_exists


def get_author_subscription_issues(sub, tzinfo, start_dt, end_dt, cache_valid_to):
    cache_key = "author_issues_{}{}_{}-{}".format(
        sub.author, '|' + sub.topic.slug if sub.topic else '',
        int(start_dt.timestamp()),
        int(end_dt.timestamp() if cache_valid_to is None else cache_valid_to)
    )

    # there is still place to improve it using get_many or redis directly
    cached_issues = cache.get(cache_key)
    if cached_issues:
        return json.loads(cached_issues)

    dt = start_dt
    intervals = []
    while True:
        interval = sub.get_period_interval(dt, tzinfo)
        if start_dt <= interval.end < end_dt:
            intervals.append(interval)
            dt = interval.end
        else:
            break

    if not intervals:
        return []

    posts_query = Post.objects.filter(
        author=sub.author,
        published__gte=intervals[0].start,
        published__lt=intervals[0].end,
    )

    if sub.topic:
        posts_query = posts_query.filter(topics=sub.topic)

    posts = peekable(posts_query.order_by('published'))

    issues = []
    for interval in intervals:
        interval_posts = []
        try:
            while posts.peek().published < interval.end:
                interval_posts.append(next(posts))
        except StopIteration:
            pass

        if interval_posts:
            issue_title = interval.title + ' summary'
            suffix = '|' + sub.topic.slug if sub.topic else ''
            isodate = str(interval.end)
            issues.append({
                'id': '{}{}-{}'.format(sub.author.username, suffix, isodate),
                'type': 'author',
                'title': issue_title,
                'time': isodate,
                'author': sub.author.to_json(topic=sub.topic),
                'posts': [p.to_json(short=True, tzinfo=tzinfo) for p in interval_posts],
            })

    if cache_valid_to is None:
        timeout = None
    else:
        timeout = max(0, cache_valid_to - int(time.time()))
    cache.set(cache_key, json.dumps(issues), timeout)
    return issues
