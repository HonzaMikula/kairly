import time
import pickle
from datetime import datetime, date, timedelta
from datetime import tzinfo as t_tzinfo
from itertools import chain
from operator import itemgetter
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
from utils.json import datetime_isoformat_ecma262, Entities, entities_json_response
from .models import Issue, Post, Subscription, SubscriptionToAuthor, Newspaper, get_newspaper_full_name
from .period import PeriodMixin
from users.models import User, ExploreTimeline

DAY_START_HOUR = 6


@dataclass
class TimelinePeriod:
    naive_date: date
    start: datetime
    end: datetime
    tzinfo: t_tzinfo
    recent_day: bool
    cache_valid_to: int

    @property
    def timeout(self):
        if self.cache_valid_to is None:
            return None
        return max(0, self.cache_valid_to - int(time.time()))


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

        issues = list(sorted(
            chain(newspaper_issues, author_issues),
            key=itemgetter('time'), reverse=True))

        # get recommended iss before stripping internal keys
        if request.user.is_authenticated:
            recommended_public_ids = self.get_recommended_public_ids(request, newspaper_issues)
        else:
            recommended_public_ids = None

        for issue in issues:
            issue.pop('$', None)  # strip internal keys

        return {
            'date': str(period.naive_date),
            'issues': issues,
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
            end_dt = now
        else:
            cache_valid_to = None

        return TimelinePeriod(d, start_dt, end_dt, tzinfo, recent_day, cache_valid_to)

    def get_links(self, period):
        links = {
            'prev': str(period.naive_date - timedelta(days=1))
        }
        if not period.recent_day:
            links['next'] = str(period.naive_date + timedelta(days=1))
        return links

    def get_recommended_public_ids(self, request, newspaper_issues):
        newspaper_issue_ids = []
        regular_newspaper_issues = []
        for issue in newspaper_issues:
            try:
                newspaper_issue_ids.append(issue['$']['id'])
                regular_newspaper_issues.append(issue)
            except KeyError:
                pass

        # find which issues wad recommented by used and which not
        # this allows showing recommend button in proper state
        # TODO should be this keeps as part of timeline endpoint
        #      can we load it independently and spedd up timeline rendering
        recommendations_query = Post.objects.filter(
            author=request.user, kind=Post.RECOMMENDATION,
            ref_issue_id__in=newspaper_issue_ids).values_list('ref_issue_id', flat=True)
        recommended_internal_ids = set(recommendations_query)
        recommended_public_ids = []
        for issue in regular_newspaper_issues:
            if issue['$']['id'] in recommended_internal_ids:
                recommended_public_ids.append(issue['id'])

        return recommended_public_ids

    def get_newspaper_issues(self, request, timeline_ctx, now, period, entities):
        subscriptions = self.get_newspaper_subscriptions(request, timeline_ctx, now)

        issues = []
        subscription_exists = False
        for sub in subscriptions:
            subscription_exists = True
            newspaper_issues = self.get_newspaper_subscription_issues(sub, period, entities)

            if sub.suspended:
                for issue in newspaper_issues:
                    issue['id'] = issue['id'].replace('.unreleased', '') + '.suspended'
                    issue['type'] = 'suspended-newspaper'
                    issue['posts'] = []

            issues.extend(newspaper_issues)

        return issues, subscription_exists

    def get_newspaper_subscription_issues(self, sub, period, entities):
        newspaper_name = "{}/{}".format(sub.newspaper.editor.username, sub.newspaper.slug)
        cache_key = "newspaper_issues_{}_{}-{}".format(
            newspaper_name,
            int(period.start.timestamp()),
            int(period.end.timestamp() if period.cache_valid_to is None else period.cache_valid_to)
        )

        cached = cache.get(cache_key)
        if cached:
            issue_entities, cached_issues = pickle.loads(cached)
            entities.update(issue_entities)
            return cached_issues

        expected_issues = set()
        dt = period.start
        while dt < period.end:
            newspaper_period = sub.newspaper.get_period_interval(dt, period.tzinfo)
            if period.start <= newspaper_period.end < period.end:
                expected_issues.add(newspaper_period.end)
            dt = newspaper_period.end

        issue_entities = Entities(user=entities.user, tzinfo=entities.tzinfo)
        query = Issue.objects.filter(
            published__gte=period.start, published__lt=period.end,
            newspaper=sub.newspaper
        )

        issues = []
        for issue in query:
            issue_json = issue.to_json(issue_entities)
            issue_json['$'] = {'id': issue.id}  # internal keys, we want to cache it but it will be stripped on response
            issues.append(issue_json)
            try:
                expected_issues.remove(issue.published)
            except KeyError:
                pass

        for missing in expected_issues:
            issue_entities.add(Newspaper, sub.newspaper_id)
            issues.append({
                "id": '{}/{}.unreleased'.format(get_newspaper_full_name(sub.newspaper_id), int(missing.timestamp())),
                "type": 'unreleased-newspaper',
                "newspaper": get_newspaper_full_name(sub.newspaper_id),
                "time": datetime_isoformat_ecma262(missing.astimezone(period.tzinfo)),
                "posts": []
            })

        cache.set(cache_key, pickle.dumps([issue_entities, issues]), period.timeout)
        entities.update(issue_entities)
        return issues

    def get_author_issues(self, request, timeline_ctx, now, period, entities):
        subscriptions = self.get_author_subscriptions(request, timeline_ctx, now)

        issues = []
        subscription_exists = False

        for sub in subscriptions:
            subscription_exists = True
            issues.extend(
                self.get_author_subscription_issues(sub, period, entities)
            )

        return issues, subscription_exists

    def get_author_subscription_issues(self, sub, period, entities):
        cache_key = "author_issues_{}_{}_{}-{}".format(
            sub.author,
            sub.get_period_uid(),
            int(period.start.timestamp()),
            int(period.end.timestamp() if period.cache_valid_to is None else period.cache_valid_to)
        )

        if not sub.suspended:
            # for suspended issue we must find just first interval and return
            # suspended placeholder instead

            # there is still place to improve it using get_many or redis directly
            cached = cache.get(cache_key)
            if cached:
                issue_entities, cached_issues = pickle.loads(cached)
                entities.update(issue_entities)
                return cached_issues

        dt = period.start
        intervals = []
        while True:
            interval = sub.get_period_interval(dt, period.tzinfo)
            if period.start <= interval.end < period.end:
                intervals.append(interval)
                dt = interval.end
            else:
                break

        if not intervals:
            return []

        if sub.suspended:
            interval = intervals[0]
            isodate = datetime_isoformat_ecma262(interval.end)
            entities.add(User, sub.author_id)
            return [{
                "id": '{}/${}/{}.suspended'.format(sub.author.username, sub.period, int(interval.end.timestamp())),
                "type": 'suspended-author',
                'title': interval.title,
                'time': isodate,
                'author': sub.author.username,
                "posts": []
            }]

        posts_query = Post.objects.filter(
            author=sub.author,
            draft=False,
            published__gte=intervals[0].start,
            published__lt=intervals[-1].end,
            hidden=False
        ).select_related('author')

        posts = peekable(posts_query.order_by('published'))
        issue_entities = Entities(user=entities.user, tzinfo=period.tzinfo)

        def post_to_json(author, post):
            if author.kind == User.FEED and post.kind == Post.RECOMMENDATION and post.ref_post:
                return post.ref_post.to_json(issue_entities, short=True)
            return {
                'post': post.to_json(issue_entities, short=True),
                'editorial': None
            }

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
                issue_entities.add(User, sub.author_id)
                issues.append({
                    'id': '{}/${}/{}'.format(sub.author.username, sub.period, int(interval.end.timestamp())),
                    'type': 'author',
                    'title': interval.title,
                    'time': isodate,
                    'author': sub.author.username,
                    'posts': [post_to_json(sub.author, p) for p in interval_posts],
                })

        cache.set(cache_key, pickle.dumps([issue_entities, issues]), period.timeout)
        entities.update(issue_entities)
        return issues


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
            return HttpResponseBadRequest(str(e))

    def get_newspaper_subscriptions(self, request, timeline_ctx, now):
        return Subscription.objects.filter(
            Q(valid_to__gt=now) | Q(renewal=True) | Q(suspended=True),
            user=request.user,
        ).select_related('newspaper', 'newspaper__editor')

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
