import time
from datetime import datetime, date, timedelta
from datetime import tzinfo as t_tzinfo
from itertools import chain
from operator import attrgetter
from dataclasses import dataclass

import dateutil.parser
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from more_itertools import peekable
from pytz import timezone

from utils.decorators import ajax_login_required
from utils.json import datetime_isoformat_ecma262, entities_json_response, MappedRef
from .models import Issue, Post, Subscription, SubscriptionToAuthor, Newspaper
from .period import PeriodMixin
from users.models import User, ExploreTimeline

DAY_START_HOUR = 6


@dataclass
class TimelinePeriod:
    naive_date: date
    start: datetime
    end: datetime
    effective_end: datetime
    tzinfo: t_tzinfo
    recent_day: bool
    cache_valid_to: int

    @property
    def timeout(self):
        if self.cache_valid_to is None:
            return None
        return max(0, self.cache_valid_to - int(time.time()))


@dataclass(eq=False)
class NewspaperTimelineIssue:
    issue_id: int
    newspaper_id: int
    number: int
    published: datetime
    json: dict = None

    @property
    def cache_key(self):
        return "newspaper_issue_{}_{}".format(self.newspaper_id, self.number)


@dataclass(eq=False)
class AuthorTimelineIssue:
    subscription: object
    interval: object
    json: dict = None

    @property
    def published(self):
        return self.interval.end

    @property
    def cache_key(self):
        return "author_issue_{}_{}_{}".format(
            self.subscription.author_id,
            self.subscription.get_period_uid(),
            int(self.published.timestamp()),
        )


class BaseTimelineView(View):

    def get_timeline(self, request, entities, timeline_ctx):
        # Group author issues by period defined by client local zone
        # It means that timeline for same user may differ when user is in different
        # timezone.
        # tzinfo = request.user.tzinfo

        # HACK for now use CET timezone to all users, until UI is improved to handle users in diferent zones
        tzinfo = timezone('Europe/Prague')
        entities.tzinfo = tzinfo

        now = datetime.now(tzinfo)

        period = self.get_timeline_period(request, now, tzinfo)

        if period.start > now:
            raise ValueError("Invalid date.")

        newspaper_issues, newspaper_subscription_exists = self.get_newspaper_issues(request, timeline_ctx, now, period, entities)
        author_issues, author_subscription_exists = self.get_author_issues(request, timeline_ctx, now, period, entities)

        if not newspaper_subscription_exists and not author_subscription_exists:
            # no subscription exists
            return None

        cached = cache.get_many([ti.cache_key for ti in chain(newspaper_issues, author_issues) if ti.json is None])
        missing_newspaper_issues = {}
        missing_author_issues = {}

        for ti in newspaper_issues:
            if ti.json is None:
                cached_issue = cached.get(ti.cache_key)
                if cached_issue:
                    references, issue_json = cached_issue
                    entities.add_references(references)
                    ti.json = issue_json
                else:
                    missing_newspaper_issues[ti.issue_id] = ti
                    #   [(ti.subscription.newspaper_id, ti.published)] = ti

        for ti in author_issues:
            if ti.json is None:
                cached_issue = cached.get(ti.cache_key)
                if cached_issue:
                    references, issue_json = cached_issue
                    entities.add_references(references)
                    ti.json = issue_json
                else:
                    missing_author_issues.setdefault(ti.subscription.author_id, []).append(ti)

        save_to_cache = {}

        if missing_newspaper_issues:
            query = Issue.objects.filter(id__in=list(missing_newspaper_issues.keys()))
            for issue in query:
                ti = missing_newspaper_issues[issue.id]
                entities.track_references = set()
                ti.json = issue.to_json(entities)
                save_to_cache[ti.cache_key] = (entities.track_references, ti.json)
                entities.track_references = None

        if missing_author_issues:
            q = None
            for author_id, issues in missing_author_issues.items():
                i = None
                for ti in issues:
                    if i is None:
                        i = [ti.interval.start, ti.interval.end]
                    else:
                        i[0] = min(i[0], ti.interval.start)
                        i[1] = max(i[1], ti.interval.end)

                q_item = Q(author_id=author_id, published__gte=i[0], published__lt=i[1])
                q = q_item if q is None else q | q_item

            posts_query = Post.objects.filter(Q(draft=False, hidden=False), q)
            posts = list(posts_query.order_by('published'))

            for author_id, issues in missing_author_issues.items():
                loaded_posts = peekable(p for p in posts if p.author_id == author_id)
                for ti in issues:
                    issue_posts = []
                    try:
                        while loaded_posts.peek().published < ti.interval.end:
                            issue_posts.append(next(loaded_posts))
                    except StopIteration:
                        pass

                    if issue_posts:
                        entities.track_references = set()
                        isodate = datetime_isoformat_ecma262(ti.interval.end)
                        author_ref = entities.make_ref(User, author_id)
                        ti.json = {
                            'id': MappedRef(author_ref, f'{{}}/${ti.subscription.period}/{int(ti.published.timestamp())}'),
                            'type': 'author',
                            'title': ti.interval.title,
                            'time': isodate,
                            'author': author_ref,
                            'posts': [post.to_json(entities, short=True) for post in issue_posts],
                            'layout': [{'post': post.id} for post in issue_posts]
                        }
                        save_to_cache[ti.cache_key] = (entities.track_references, ti.json)
                        entities.track_references = None
                    else:
                        save_to_cache[ti.cache_key] = ([], None)

        if save_to_cache:
            cache.set_many(save_to_cache, period.timeout)

        issues = sorted(
            (issue for issue in chain(newspaper_issues, author_issues) if issue.json is not None),
            key=attrgetter('published'), reverse=True)

        # get recommended ids before stripping internal keys
        if request.user.is_authenticated:
            recommended_public_ids = self.get_recommended_public_ids(request, newspaper_issues, entities)
        else:
            recommended_public_ids = None

        return {
            'date': str(period.naive_date),
            'issues': [ti.json for ti in issues],
            'links': self.get_links(period),
            'validTo': period.cache_valid_to,
            'recommended': recommended_public_ids,
        }

    def get_newspaper_subscriptions(self, request, timeline_ctx, now):
        raise NotImplementedError

    def get_author_subscriptions(self, request, timeline_ctx, now):
        raise NotImplementedError

    def get_timeline_period(self, request, now, tzinfo):
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

        recent_day = now < end_dt + timedelta(hours=DAY_START_HOUR)

        if recent_day and now < end_dt:
            cache_valid_to = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            cache_valid_to = int(cache_valid_to.timestamp())
            effective_end_dt = now
        else:
            cache_valid_to = None
            effective_end_dt = end_dt

        return TimelinePeriod(d, start_dt, end_dt, effective_end_dt, tzinfo, recent_day, cache_valid_to)

    def get_links(self, period):
        links = {
            'prev': str(period.naive_date - timedelta(days=1))
        }
        if not period.recent_day:
            links['next'] = str(period.naive_date + timedelta(days=1))
        return links

    def get_recommended_public_ids(self, request, newspaper_issues, entities):
        """find which issues was recommented by used and which not
         this allows showing recommend button in proper state
         TODO should be this keeps as part of timeline endpoint
              can we load it independently and spedd up timeline rendering
        """
        newspaper_issue_ids = []
        ti_by_id = {}
        for ti in newspaper_issues:
            newspaper_issue_ids.append(ti.issue_id)
            ti_by_id[ti.issue_id] = ti

        recommendations_query = Post.objects.filter(
            author=request.user, kind=Post.RECOMMENDATION,
            ref_issue_id__in=newspaper_issue_ids).values_list('ref_issue_id', flat=True)

        recommended_public_ids = []
        for issue_id in recommendations_query:
            ti = ti_by_id[issue_id]
            if ti.json is not None:
                recommended_public_ids.append(ti.json['id'])

        return recommended_public_ids

    def get_newspaper_issues(self, request, timeline_ctx, now, period, entities):
        subscriptions = self.get_newspaper_subscriptions(request, timeline_ctx, now)

        subscription_exists = False
        newspaper_ids = []
        suspended_newspaper_ids = set()
        for sub in subscriptions:
            subscription_exists = True
            newspaper_ids.append(sub.newspaper_id)
            if sub.suspended:
                suspended_newspaper_ids.add(sub.newspaper_id)

        query = Issue.objects.filter(
            published__gte=period.start, published__lt=period.effective_end,
            newspaper_id__in=newspaper_ids
        ).values_list('id', 'newspaper_id', 'number', 'published')

        issues = []
        for issue_id, newspaper_id, number, published in query:
            ti = NewspaperTimelineIssue(issue_id, newspaper_id, number, published)
            if newspaper_id in suspended_newspaper_ids:
                newspaper_ref = entities.make_ref(Newspaper, newspaper_id)
                ti.json = {
                    "id": MappedRef(newspaper_ref, f'{{}}/{int(ti.published.timestamp())}.suspended'),
                    "type": 'suspended-newspaper',
                    "newspaper": newspaper_ref,
                    "time": datetime_isoformat_ecma262(ti.published.astimezone(period.tzinfo)),
                    "posts": [],
                    "layout": []
                }
            issues.append(ti)

        return issues, subscription_exists

    def get_author_issues(self, request, timeline_ctx, now, period, entities):
        subscriptions = self.get_author_subscriptions(request, timeline_ctx, now)

        issues = []
        subscription_exists = False

        for sub in subscriptions:
            subscription_exists = True

            if sub.suspended:
                author_ref = entities.make_ref(User, sub.author_id)

            dt = period.start
            while True:
                interval = sub.get_period_interval(dt, period.tzinfo)
                if period.start <= interval.end < period.effective_end:
                    ti = AuthorTimelineIssue(sub, interval)
                    issues.append(ti)

                    if sub.suspended:
                        ti.json = {
                            'id': MappedRef(author_ref, f'{{}}/${sub.period}/{int(interval.end.timestamp())}.suspended'),
                            'type': 'suspended-author',
                            'title': interval.title,
                            'time': datetime_isoformat_ecma262(interval.end),
                            'author': author_ref,
                            'posts': [],
                            'layout': []
                        }
                        break

                    dt = interval.end
                else:
                    break

        return issues, subscription_exists


class TimelineView(BaseTimelineView):

    @ajax_login_required
    @method_decorator(entities_json_response)
    def get(self, request, entities):
        try:
            timeline = self.get_timeline(request, entities, None)
            if timeline is None:
                return HttpResponse(status=204)
            else:
                return timeline
        except ValueError as e:
            raise e
            return HttpResponseBadRequest(str(e))

    def get_newspaper_subscriptions(self, request, timeline_ctx, now):
        return Subscription.objects.filter(
            Q(valid_to__gt=now) | Q(renewal=True) | Q(suspended=True),
            user=request.user,
        ).select_related('newspaper')

    def get_author_subscriptions(self, request, timeline_ctx, now):
        return SubscriptionToAuthor.objects.filter(
            Q(valid_to__gt=now) | Q(renewal=True) | Q(suspended=True),
            user=request.user
        ).select_related('author')


@dataclass
class SubscriptionMock:
    newspaper: Newspaper

    @property
    def suspended(self):
        return False

    @property
    def newspaper_id(self):
        return self.newspaper.id


@dataclass
class SubscriptionToAuthorMock(PeriodMixin):
    author: User
    period: str
    period_time: object
    period_dow: int

    @property
    def suspended(self):
        return False

    @property
    def author_id(self):
        return self.author.id


class ExploreTimelineView(BaseTimelineView):

    @method_decorator(entities_json_response)
    def get(self, request, entities, tab):
        try:
            explore = get_object_or_404(ExploreTimeline, slug=tab)
            timeline = self.get_timeline(request, entities, explore)
            if timeline is None:
                return HttpResponse(status=204)
            else:
                return timeline
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

    def get_newspaper_subscriptions(self, request, explore, now):
        q = None
        for newspaper_id in explore.content['newspapers']:
            username, slug = newspaper_id.split('/')
            _q = Q(editor__username=username, slug=slug)
            q = _q if q is None else q | _q

        if q is None:
            return []

        return [SubscriptionMock(n) for n in Newspaper.objects.filter(q)]

    def get_author_subscriptions(self, request, explore, now):
        ids = set()
        for cat in explore.content['authors']:
            for author_id in cat['authors']:
                ids.add(author_id)

        subscriptions = []
        for user in User.objects.filter(username__in=list(ids)):
            subscriptions.append(SubscriptionToAuthorMock(user, PeriodMixin.X6_PER_DAY, None, None))

        return subscriptions
