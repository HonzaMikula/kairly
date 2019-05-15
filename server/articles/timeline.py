import time
from datetime import datetime, timedelta
from itertools import chain
from operator import itemgetter

import dateutil.parser
import rapidjson as json
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from more_itertools import peekable
from utils.decorators import ajax_login_required
from utils.json import JsonResponse, datetime_isoformat_ecma262

from .models import Issue, Post, Subscription, SubscriptionToAuthor
from users.models import User

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

    newspaper_issue_ids = []
    regular_newspaper_issues = []
    for issue in newspaper_issues:
        try:
            newspaper_issue_ids.append(issue['$']['id'])
            regular_newspaper_issues.append(issue)
        except KeyError:
            pass

    recommendations_query = Post.objects.filter(
        author=request.user, kind=Post.RECOMMENDATION,
        ref_issue_id__in=newspaper_issue_ids).values_list('ref_issue_id', flat=True)
    recommended_internal_ids = set(recommendations_query)
    recommended_public_ids = []
    for issue in regular_newspaper_issues:
        if issue['$']['id'] in recommended_internal_ids:
            recommended_public_ids.append(issue['id'])

    issues = list(sorted(
        chain(newspaper_issues, author_issues),
        key=itemgetter('time'), reverse=True))

    for issue in issues:
        issue.pop('$', None)  # strip internal keys

    return JsonResponse({
        'date': str(d),
        'issues': issues,
        'links': links,
        'validTo': cache_valid_to,
        'recommended': recommended_public_ids,
    })


def get_newspaper_issues(request, now, tzinfo, start_dt, end_dt, cache_valid_to):
    subscriptions = Subscription.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True) | Q(suspended=True),
        user=request.user,
    ).select_related('newspaper', 'newspaper__editor')

    issues = []
    subscription_exists = False
    for sub in subscriptions:
        subscription_exists = True
        newspaper_issues = get_newspaper_subscription_issues(sub, tzinfo, start_dt, end_dt, cache_valid_to)

        if sub.suspended:
            for issue in newspaper_issues:
                issue['id'] = issue['id'].replace('.unreleased', '') + '.suspended'
                issue['type'] = 'suspended-newspaper'
                issue['posts'] = []

        issues.extend(newspaper_issues)

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

    expected_issues = set()
    dt = start_dt
    while dt < end_dt:
        period = sub.newspaper.get_period_interval(dt, tzinfo)
        if start_dt <= period.end < end_dt:
            expected_issues.add(period.end)
        dt = period.end

    query = Issue.objects.filter(
        published__gte=start_dt, published__lt=end_dt,
        newspaper=sub.newspaper
    )

    issues = []
    for issue in query:
        issue_json = issue.to_json(newspaper=sub.newspaper, tzinfo=tzinfo)
        issue_json['$'] = {'id': issue.id}  # internal keys, want ot cache but will be stripped on response
        issues.append(issue_json)
        try:
            expected_issues.remove(issue.published)
        except KeyError:
            pass

    for missing in expected_issues:
        issues.append({
            "id": '{}/{}.unreleased'.format(sub.newspaper.full_name, int(missing.timestamp())),
            "type": 'unreleased-newspaper',
            "newspaper": sub.newspaper.to_json(tzinfo),  # TODO return newspapers separately, as done alredy for subscriptions
            "time": datetime_isoformat_ecma262(missing.astimezone(tzinfo)),
            "posts": []
        })

    if cache_valid_to is None:
        timeout = None
    else:
        timeout = max(0, cache_valid_to - int(time.time()))
    cache.set(cache_key, json.dumps(issues), timeout)
    return issues


def get_author_issues(request, now, tzinfo, start_dt, end_dt, cache_valid_to):
    subscriptions = SubscriptionToAuthor.objects.filter(
        Q(valid_to__gt=now) | Q(renewal=True) | Q(suspended=True),
        user=request.user
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
    cache_key = "author_issues_{}_{}_{}-{}".format(
        sub.author,
        sub.get_period_uid(),
        int(start_dt.timestamp()),
        int(end_dt.timestamp() if cache_valid_to is None else cache_valid_to)
    )

    if not sub.suspended:
        # for suspended issue we must find just first interval and return
        # suspended placeholder instead

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

    if sub.suspended:
        interval = intervals[0]
        isodate = datetime_isoformat_ecma262(interval.end)
        return [{
            "id": '{}/${}/{}.suspended'.format(sub.author.username, sub.period, int(interval.end.timestamp())),
            "type": 'suspended-author',
            'title': interval.title,
            'time': isodate,
            'author': sub.author.to_json(),
            "posts": []
        }]

    posts_query = Post.objects.filter(
        author=sub.author,
        draft=False,
        published__gte=intervals[0].start,
        published__lt=intervals[-1].end,
        hidden=False
    )

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
            isodate = datetime_isoformat_ecma262(interval.end)
            issues.append({
                'id': '{}/${}/{}'.format(sub.author.username, sub.period, int(interval.end.timestamp())),
                'type': 'author',
                'title': interval.title,
                'time': isodate,
                'author': sub.author.to_json(),
                'posts': [p.to_json(short=True, tzinfo=tzinfo) for p in interval_posts],
            })

    if cache_valid_to is None:
        timeout = None
    else:
        timeout = max(0, cache_valid_to - int(time.time()))
    cache.set(cache_key, json.dumps(issues), timeout)
    return issues
