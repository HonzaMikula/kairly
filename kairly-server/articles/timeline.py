from operator import itemgetter
from itertools import chain
from datetime import datetime, timedelta
import dateutil.parser

from more_itertools import peekable

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

    if recent_day:
        valid_to = end_dt.timestamp()
    else:
        valid_to = None
        links['next'] = str(d + timedelta(days=1))

    end_dt = min(now, end_dt)

    newspaper_issues, newspaper_subscription_exists = get_newspaper_issues(
        request, now, tzinfo, start_dt, end_dt)

    author_issues, author_subscription_exists = get_author_issues(
        request, now, tzinfo, start_dt, end_dt)

    if not newspaper_subscription_exists and not author_subscription_exists:
        # no subscription exists
        return HttpResponse(status=204)

    issues = list(sorted(
        chain(newspaper_issues, author_issues),
        key=itemgetter('time'), reverse=True))

    return JsonResponse({
        'date': str(d),
        'validTo': valid_to,
        'issues': issues,
        'links': links,
    })


def get_newspaper_issues(request, now, tzinfo, start_dt, end_dt):
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
            get_newspaper_subscription_issues(sub, tzinfo, start_dt, end_dt)
        )
    return issues, subscription_exists


def get_newspaper_subscription_issues(sub, tzinfo, start_dt, end_dt):
    query = Issue.objects.filter(
        published__gte=start_dt, published__lt=end_dt,
        newspaper=sub.newspaper
    )

    issues = []
    for issue in query:
        issues.append(issue.to_json(
            newspaper=sub.newspaper,
            tzinfo=tzinfo))
    return issues


def get_author_issues(request, now, tzinfo, start_dt, end_dt):
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
            get_author_subscription_issues(sub, tzinfo, start_dt, end_dt)
        )

    return issues, subscription_exists


def get_author_subscription_issues(sub, tzinfo, start_dt, end_dt):
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

    posts = peekable(Post.objects.filter(
        author=sub.author,
        published__gte=intervals[0].start,
        published__lt=intervals[0].end,
    ).order_by('published'))

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
    return issues
