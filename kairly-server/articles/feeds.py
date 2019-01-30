from django.conf import settings
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import DefaultFeed

from .period import PeriodMixin
from .models import Newspaper, Issue


class ImageRssFeedGenerator(DefaultFeed):
    def add_root_elements(self, handler):
        super(ImageRssFeedGenerator, self).add_root_elements(handler)
        if 'image_url' in self.feed:
            handler.startElement(u'image', {})
            handler.addQuickElement(u"url", self.feed['image_url'])
            handler.addQuickElement(u"title", self.feed['title'])
            handler.addQuickElement(u"link", self.feed['link'])
            handler.endElement(u'image')


class NewspaperFeed(Feed):
    feed_type = ImageRssFeedGenerator

    def get_object(self, request, username, newspapeper_slug):
        return get_object_or_404(Newspaper, editor__username=username, slug=newspapeper_slug)

    def feed_extra_kwargs(self, newspaper):
        if newspaper.image:
            return {
                'image_url': f"https://cdn.kairly.com{settings.MEDIA_URL}{newspaper.image}"
            }
        return {}

    def title(self, newspaper):
        return newspaper.title

    def link(self, newspaper):
        return f"https://kairly.com/{newspaper.full_name}"

    def description(self, newspaper):
        return newspaper.description

    def items(self, newspaper):
        query = Issue.objects.filter(newspaper=newspaper).order_by('-number')[:10]
        return [(newspaper, issue) for issue in query]

    def item_link(self, newspaper_issue):
        newspaper, issue = newspaper_issue
        return f"https://kairly.com/{newspaper.full_name}/{issue.number}"

    def item_title(self, newspaper_issue):
        newspaper, issue = newspaper_issue
        if newspaper.period in [PeriodMixin.X6_PER_DAY, PeriodMixin.X3_PER_DAY]:
            return f"{newspaper.title} ~ {issue.published:%d. %m. %Y %H:%M}"
        else:
            return f"{newspaper.title} ~ {issue.published:%d. %m. %Y}"

    def item_pubdate(self, newspaper_issue):
        newspaper, issue = newspaper_issue
        return issue.published
