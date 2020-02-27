import json

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import DefaultFeed

from .period import PeriodMixin
from .models import Newspaper, Issue, Post


class RssFeedGenerator(DefaultFeed):
    def rss_attributes(self):
        attrs = super().rss_attributes()
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        return attrs

    def add_root_elements(self, handler):
        self.feed['language'] = None

        super().add_root_elements(handler)
        if 'image_url' in self.feed:
            handler.startElement('image', {})
            handler.addQuickElement("url", self.feed['image_url'])
            handler.addQuickElement("title", self.feed['title'])
            handler.addQuickElement("link", self.feed['link'])
            handler.endElement('image')

        handler.addQuickElement("dc:creator", self.feed['author_name'])

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement("dc:creator", self.feed['author_name'])


class NewspaperFeed(Feed):
    feed_type = RssFeedGenerator

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

    def author_name(self, newspaper):
        return newspaper.editor.name or newspaper.editor.username

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

    def item_description(self, newspaper_issue):
        newspaper, issue = newspaper_issue
        titles = []
        for post in issue.posts.all():
            if post.kind == Post.TWEET:
                if post.author:
                    name = post.author.name or post.author.username
                else:
                    for attachment in json.loads(post.attachments):
                        if attachment['type'] == 'author':
                            name = attachment['screen_name']
                            break
                titles.append(name + "'s tweet")
            else:
                if post.title:
                    titles.append(post.title)
        return ' • '.join(titles)
