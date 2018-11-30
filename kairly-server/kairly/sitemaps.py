from datetime import datetime, timezone
from django.contrib.sitemaps import Sitemap
from django.utils.timezone import now as timezone_now

from articles.models import Newspaper, Issue, Post
from articles.period import PeriodMixin


class NewspaperSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Newspaper.objects.all().select_related('editor')

    def location(self, obj):
        return '/' + obj.full_name

    def changefreq(self, obj):
        if obj.period == PeriodMixin.WEEKLY:
            return 'weekly'
        if obj.period == PeriodMixin.DAILY:
            return 'daily'
        return 'hourly'

    def lastmod(self, obj):
        try:
            issue = Issue.objects.filter(newspaper=obj).order_by('-number')[0]
            return issue.published
        except IndexError:
            return None


class PostSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Post.objects.filter(
            kind=Post.NEWSPAPER,
            draft=False,
            published__lt=timezone_now(),
            published__gt=datetime(2018, 11, 1, 0, 0, 0, tzinfo=timezone.utc),
            source__isnull=True
        ).exclude(
            author__username__in=['kairly-newuser']
        ).select_related('author')

    def location(self, obj):
        return '/{}/{}'.format(obj.author.username, obj.slug)

    def changefreq(self, obj):
        return 'never'

    def lastmod(self, obj):
        return obj.published
