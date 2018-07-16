from datetime import datetime, timedelta, timezone

from more_itertools import peekable

from django.http import JsonResponse

from users.models import User
from utils.decorators import ajax_login_required
from .models import EditionIssue, Post, Edition, SubscriptionToAuthor


TIMELINE_PAGE_SIZE = 6


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

    def __init__(self, before, tzinfo):
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


class EditionIssueItem(TimelineItem):

    def __init__(self, issue, edition, tzinfo):
        super().__init__(issue.published.astimezone(tzinfo))
        self.issue = issue
        self.edition = edition
        self.tzinfo = tzinfo

    @property
    def json(self):
        return self.issue.to_json(
            edition=self.edition,
            tzinfo=self.tzinfo
        )


class EditionIssueStream(TimelineStream):

    QUERY_PAGE_SIZE = TIMELINE_PAGE_SIZE

    def __init__(self, user, before, tzinfo):
        super().__init__(before, tzinfo)
        self.user = user

    def __iter__(self):
        editions = {e.id: e for e in Edition.objects.filter(subscription__user=self.user)}
        query = EditionIssue.objects.filter(published__lt=self.before, edition_id__in=editions.keys())
        for issue in QueryIterator(query, self.QUERY_PAGE_SIZE):
            yield EditionIssueItem(issue, editions[issue.edition_id], self.tzinfo)


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

    def __init__(self, author, subscription, before, tzinfo):
        super().__init__(before, tzinfo)
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
            published = post['published'].astimezone(self.tzinfo)
            _, end, title = self.subscription.get_issue_interval(published)
            if issue_end != end:
                # Post from "unpublished" summary may already exists in database
                # Or due paging, some post individua may be published before self.before
                # but their interval belong to prev page and not match time condition
                if post_ids and issue_end < self.before:
                    yield AuthorIssueItem(
                        issue_end, issue_title, self.author,
                        self.subscription.topic, post_ids, self.tzinfo)
                post_ids = []
                issue_end = end
                issue_title = title
            post_ids.append(post['id'])

        if post_ids:
            yield AuthorIssueItem(issue_end, issue_title, self.author,
                                  self.subscription.topic, post_ids, self.tzinfo)


class AuthorsStream(TimelineStream):

    def __init__(self, user, before, tzinfo):
        super().__init__(before, tzinfo)
        self.user = user

    def __iter__(self):
        # TODO this can be probably simplified after author-user merge
        author_subscriptions = {s.id: s for s in SubscriptionToAuthor.objects.filter(user=self.user)}
        author_ids = [asub.author_id for asub in author_subscriptions.values()]
        authors = {u.id: u for u in User.objects.filter(id__in=author_ids)}

        streams = [
            AuthorStream(authors[asub.author_id], asub, self.before, self.tzinfo)
            for asub in author_subscriptions.values()
        ]
        yield from TimelineStream.merge(*streams)


@ajax_login_required
def timeline(request):
    # Group author issues by period defined by client local zone
    # It means that timeline for same user may differ when user is in different
    # timezone.

    try:
        ts = int(request.GET.get('cursor'))
        before = datetime.fromtimestamp(ts, request.tzinfo)
    except (ValueError, TypeError):
        before = datetime.now(request.tzinfo)

    issues = []
    stop_on_next = None
    timeline_stream = TimelineStream.merge(
        EditionIssueStream(request.user, before, request.tzinfo),
        AuthorsStream(request.user, before, request.tzinfo)
    )
    for item in timeline_stream:
        if stop_on_next and item.published != stop_on_next:
            break
        issues.append(item.json)
        if len(issues) >= TIMELINE_PAGE_SIZE:
            # include all other issues with same published time
            # this is requeire to make cursor working
            stop_on_next = item.published

    return JsonResponse({
        'issues': issues,
        'cursor': stop_on_next.timestamp() if stop_on_next else None
    })
