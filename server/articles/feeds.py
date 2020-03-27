import orjson as json
from typing import List
from dataclasses import dataclass

from django.conf import settings
from django.template import loader
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import DefaultFeed

from .period import PeriodMixin
from .models import Newspaper, Issue, Post


@dataclass
class AuthorItem:
    username: str
    name: str


@dataclass
class PostItem:
    kind: str
    slug: str
    author: str
    title: str
    perex: str
    content: str


@dataclass
class LayoutColumn:
    style: str
    posts: List[object]


@dataclass
class LayoutBox:
    layout: str
    columns: List[LayoutColumn]
    delimiter: str = None


@dataclass
class IssueItem:
    newspaper: object
    issue: object
    boxes: List[object]


class RssFeedGenerator(DefaultFeed):
    def rss_attributes(self):
        attrs = super().rss_attributes()
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        attrs['xmlns:content'] = "http://purl.org/rss/1.0/modules/content/"
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
        handler.addQuickElement('content:encoded', item['content_encoded'])


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
        items = []
        for issue in query:
            posts = {}
            for post in issue.posts.all().select_related('author'):
                if post.author is None:
                    author = None
                    if post.attachments:
                        attachments = json.loads(post.attachments)
                        if post.kind == Post.TWEET:
                            for attachment in json.loads(post.attachments):
                                if attachment['type'] == 'author':
                                    author = AuthorItem(None, attachment['screen_name'])
                                    break
                        else:
                            attachment = attachments.get('author')
                            if attachment:
                                author = AuthorItem(None, attachment['name'])
                else:
                    author = AuthorItem(post.author.username, post.author.name or post.author.username)

                posts[post.id] = PostItem(
                    post.kind,
                    post.slug,
                    author,
                    post.title,
                    post.perex,
                    post.content
                )

            boxes = []
            for box in json.loads(issue.layout):
                if isinstance(box, list):
                    box_layout = None
                    box_columns = []
                    for col in box:
                        # skip box layout, box is [layout: str, cols...]
                        if isinstance(col, str):
                            box_layout = col
                            continue

                        col_layout = None
                        col_posts = []
                        for item in col:
                            # skip column class, columns is [cls: str, items...]
                            if isinstance(item, str):
                                col_layout = item
                                continue

                            post_id = item.get('post')
                            if post_id:
                                col_posts.append(posts[post_id])

                        box_columns.append(LayoutColumn(col_layout, col_posts))

                    boxes.append(LayoutBox(box_layout, box_columns))
                else:
                    post_id = box.get('post')
                    if post_id:
                        boxes.append(LayoutBox(None, [LayoutColumn(None, [posts[post_id]])]))

            items.append(IssueItem(newspaper, issue, boxes))
        return items

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_link(self, item):
        return f"https://kairly.com/{item.newspaper.full_name}/{item.issue.number}"

    def item_title(self, item):
        titles = self.get_post_titles(item)
        return f"{item.newspaper.title} #{item.issue.number}: {titles[0]}"

    def item_pubdate(self, item):
        return item.issue.published

    def item_description(self, item):
        description = self.get_post_titles(item)
        description.pop(0)

        return ' • '.join(description)

    def get_post_titles(self, item):
        titles = []

        def get_post_title(post):
            if post.kind == Post.TWEET:
                if post.author:
                    return f"{post.author.name}: {post.content[:50]}"
            else:
                if post.title:
                    return post.title

        for box in item.boxes:
            for col in box.columns:
                for post in col.posts:
                    title = get_post_title(post)
                    if title:
                        titles.append(title)
        
        return titles
      

    def item_content_encoded(self, item):
        template = loader.get_template('articles/feed-content.html')
        return template.render({'item': item})
