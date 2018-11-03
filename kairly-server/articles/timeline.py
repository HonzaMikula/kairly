from datetime import datetime, timezone, timedelta
import dateutil.parser

from more_itertools import peekable

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from users.models import User
from utils.decorators import ajax_login_required
from .models import Issue, Post, Newspaper, Subscription, SubscriptionToAuthor


TIMELINE_PAGE_SIZE = 6
DAY_START_HOUR = 6


class QueryIterator:

    def __init__(self, query, page_size):
        self.query = query
        self.page_size = page_size

    def __iter__(self):
        page = 0
        while True:
            offset = page * self.page_size
            items = self.query[offset:offset + self.page_size]
            if items:
                yield from items
                page += 1
            else:
                break


class TimelineItem:
    """Lazy converts to JSON"""

    def __init__(self, published):
        self.published = published

    def json(self):
        raise NotImplementedError


class TimelineStream:

    def __init__(self, after, before, tzinfo):
        # TODO combine after and before into single object
        self.after = after
        self.before = before
        self.tzinfo = tzinfo

    @staticmethod
    def merge(*streams):
        streams = [peekable(s) for s in streams]

        while True:
            items = [s.peek(None) for s in streams]
            mx = datetime.fromtimestamp(1, timezone.utc)
            mx_idx = None
            for idx, item in enumerate(items):
                if item and item.published > mx:
                    mx = item.published
                    mx_idx = idx
            if mx_idx is None:
                break
            yield next(streams[mx_idx])


class NewspaperIssueItem(TimelineItem):

    def __init__(self, issue, newspaper, tzinfo):
        super().__init__(issue.published.astimezone(tzinfo))
        self.issue = issue
        self.newspaper = newspaper
        self.tzinfo = tzinfo

    @property
    def json(self):
        return self.issue.to_json(
            newspaper=self.newspaper,
            tzinfo=self.tzinfo
        )


class NewspaperIssueStream(TimelineStream):

    # QUERY_PAGE_SIZE = TIMELINE_PAGE_SIZE

    def __init__(self, user, after, before, tzinfo):
        super().__init__(after, before, tzinfo)
        now = datetime.now(self.tzinfo)

        self.subscriptions = list(Subscription.objects.filter(
            user=user, renewal=True, valid_from__lte=now, valid_to__gt=now))

    def __bool__(self):
        return bool(self.subscriptions)

    def __iter__(self):
        newspapers = {e.id: e for e in Newspaper.objects.filter(subscription__in=self.subscriptions)}
        query = Issue.objects.filter(
            published__gte=self.after, published__lt=self.before,
            newspaper_id__in=newspapers.keys()
        )
        # for issue in QueryIterator(query, self.QUERY_PAGE_SIZE):
        for issue in query:
            yield NewspaperIssueItem(issue, newspapers[issue.newspaper_id], self.tzinfo)


class AuthorIssueItem(TimelineItem):

    def __init__(self, published, title, author, topic, post_ids, tzinfo):
        super().__init__(published)
        self.title = title
        self.topic = topic
        self.author = author
        self.post_ids = post_ids
        self.tzinfo = tzinfo

    @property
    def json(self):
        posts = Post.objects.filter(id__in=self.post_ids)
        suffix = '|' + self.topic.slug if self.topic else ''
        isodate = str(self.published)
        return {
            'id': '{}{}-{}'.format(self.author.username, suffix, isodate),
            'type': 'author',
            'title': self.title,
            'time': isodate,
            'author': self.author.to_json(topic=self.topic),
            'posts': [p.to_json(short=True, tzinfo=self.tzinfo) for p in posts],
        }


class AuthorStream(TimelineStream):

    QUERY_PAGE_SIZE = 100

    def __init__(self, author, subscription, after, before, tzinfo):
        super().__init__(after, before, tzinfo)
        self.author = author
        self.subscription = subscription

    def __iter__(self):
        posts_query = Post.objects.filter(
            author_id=self.author.id,
            published__lt=self.before
        )
        if self.subscription.topic:
            posts_query = posts_query.filter(topics=self.subscription.topic)
        posts_query = posts_query.order_by('-published').values('id', 'published')

        issue_end = None
        issue_title = None
        post_ids = None

        for post in QueryIterator(posts_query, self.QUERY_PAGE_SIZE):
            interval = self.subscription.get_period_interval(post['published'], self.tzinfo)

            if issue_end != interval.end:
                # Post from "unpublished" summary may already exists in database
                # Or due paging, some post individua may be published before self.before
                # but their interval belong to prev page and not match time condition
                if post_ids and issue_end < self.before:
                    yield AuthorIssueItem(
                        issue_end, issue_title, self.author,
                        self.subscription.topic, post_ids, self.tzinfo)
                post_ids = []
                issue_end = interval.end
                issue_title = interval.title + ' summary'
            post_ids.append(post['id'])

        if post_ids:
            yield AuthorIssueItem(issue_end, issue_title, self.author,
                                  self.subscription.topic, post_ids, self.tzinfo)


class AuthorsStream(TimelineStream):

    def __init__(self, user, after, before, tzinfo):
        super().__init__(after, before, tzinfo)

        now = datetime.now(self.tzinfo)
        self.author_subscriptions = {s.id: s for s in SubscriptionToAuthor.objects.filter(
            user=user, renewal=True, valid_from__lte=now, valid_to__gt=now)}

    def __bool__(self):
        return bool(self.author_subscriptions)

    def __iter__(self):
        author_ids = [asub.author_id for asub in self.author_subscriptions.values()]
        authors = {u.id: u for u in User.objects.filter(id__in=author_ids)}

        streams = [
            AuthorStream(authors[asub.author_id], asub, self.after, self.before, self.tzinfo)
            for asub in self.author_subscriptions.values()
        ]
        yield from TimelineStream.merge(*streams)


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

    streams = [
        NewspaperIssueStream(request.user, start_dt, end_dt, tzinfo),
        AuthorsStream(request.user, start_dt, end_dt, tzinfo)
    ]

    if not any(streams):
        # no subscription exists
        return HttpResponse(status=204)

    issues = []
    timeline_stream = TimelineStream.merge(*streams)

    for item in timeline_stream:
        if item.published < start_dt:
            break
        issues.append(item.json)

    return JsonResponse({
        'date': str(d),
        'validTo': valid_to,
        'issues': issues,
        'links': links,
    })
