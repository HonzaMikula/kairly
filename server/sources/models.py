from os.path import dirname
from urllib.parse import urlsplit, urlunsplit
import rapidjson as json

import feedparser
import requests
import lxml.html


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.dispatch import receiver

from sources.parser import ArticleParser, split_article_to_perex_and_content, validate_rules
from sources.directives import validate_directives, parse as parse_directives
from utils.url import clean_url, fetch_url

from articles.models import Backlog, Post, get_newspaper_full_name
from articles.signals import post_publish


class EntryHasNoContentException(Exception):
    pass


class Channel(models.Model):
    name = models.CharField(max_length=160)
    provider = models.CharField(max_length=32, help_text="Source identifier (namespace for guid)")
    rss = models.CharField(max_length=250)
    import_links = models.BooleanField(default=False)
    parse_content_from_rss = models.BooleanField(default=False)
    user_agent = models.CharField(help_text="Force User-Agent header when fetching RSS or post", max_length=250, null=True, blank=True)
    parser = models.TextField(help_text="Parse rules to get content from webpage/rss.", blank=False, validators=[validate_rules])
    directives = models.TextField(blank=True, validators=[validate_directives])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    newspaper = models.CharField(help_text="Automatically add to newspaper's backlog", max_length=160, null=True, blank=True, db_index=True)
    enabled = models.BooleanField(default=True)
    protected = models.BooleanField(default=True, help_text="Only users logged in can see full content")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_directives(self, name, target=None):
        if not hasattr(self, '_directives'):
            self._directives = parse_directives(self.directives)

        directives = [d for d in self._directives if d.name == name]
        if target is not None:
            directives = [d for d in directives if d.target == target]
        return directives

    def save(self, *args, **kwargs):
        # validate directives
        parse_directives(self.directives)

        if self.newspaper is not None and not self.newspaper.strip():
            self.newspaper = None

        super().save(*args, **kwargs)

    def parse_rss(self):
        kwargs = {}
        if self.user_agent:
            kwargs['agent'] = self.user_agent
        return feedparser.parse(self.rss, **kwargs)

    def parse_entry(self, entry, *, usecache=False):
        htmltree, resolved_url = self.parse_html_root(entry, usecache=usecache)
        attachments = None

        video_directives = self.get_directives('video', 'poster')
        if video_directives:
            directive = video_directives[-1]
            kind = Post.VIDEO
            try:
                poster = htmltree.cssselect(directive.value)[0]
                src = poster.attrib.get('src')
                if src:
                    attachments = json.dumps([
                        {
                            'type': 'video-poster',
                            'src': src
                        }
                    ])
            except IndexError:
                pass

        else:
            kind = Post.NEWSPAPER

        parser = ArticleParser(self.parser)
        fragments = parser.parse(htmltree)
        fragments = parser.normalize(fragments)

        perex, content = split_article_to_perex_and_content(fragments, [500, 950])

        replacements = self.get_directives('replace', 'document')
        for replacement in replacements:
            perex = replacement.replace(perex)
            content = replacement.replace(content)

        return {
            'kind': kind,
            'perex': perex,
            'content': content,
            'source': resolved_url,
            'attachments': attachments
        }

    def parse_html_root(self, entry, *, usecache=False):
        parsed_url = urlsplit(entry.link)
        url = urlunsplit(parsed_url[:-1] + ("",))  # strip fragment
        html = None
        if self.parse_content_from_rss:
            # some feeds has full article in content attribute, see issue #40
            # eg http://www.mindtheproduct.com/feed/ or https://blogs.windows.com/msedgedev/feed/
            #
            # On the other hand content may contains only shortened text
            # like https://www.blog.google/products/search/rss/ for which feedparser
            # returns text/plain summary inside content attr, see issue #44
            #
            # This means that sometimes descrption is proper source otherways
            # content must be used. For now best approach seems to be use
            # content only if contains text/html type.
            if hasattr(entry, 'content'):
                for content in entry.content:
                    if content.type == 'text/html':
                        html = content.value
                        break
            if html is None:
                html = getattr(entry, 'description', None)

            if html is None:
                raise EntryHasNoContentException

            # hit document to get real url
            entry_url = entry.link.split('#', maxsplit=1)[0]
            headers = {'User-Agent': settings.DEFAULT_USER_AGENT}
            if entry_url:
                resolved_url = requests.head(entry_url, headers=headers, allow_redirects=True).url
            else:
                resolved_url = None
        else:
            html, resolved_url = fetch_url(url, usecache=usecache, user_agent=self.user_agent)

        htmltree = lxml.html.fromstring(html)
        try:
            # if descrption contains full html, dive into
            htmltree = htmltree.cssselect("body")[0]
        except IndexError:
            pass

        if entry.link:
            self.fix_relative_links(htmltree, parsed_url)

        if resolved_url:
            resolved_url = clean_url(resolved_url)

        return htmltree, resolved_url

    def is_url_valid(self, url):
        domains = [d.value for d in self.get_directives('skip', 'domain')]

        if domains:
            url = url.split('#', maxsplit=1)[0]
            return urlsplit(url).hostname not in domains
        return True

    def fix_relative_links(self, htmltree, parsed_url):
        host = '//' + parsed_url.hostname

        def fix_attr(el, attr):
            link = el.attrib.get(attr)
            if not link or link.startswith('//') or '://' in link:
                return
            if link.startswith('/'):
                el.attrib[attr] = host + link
            else:
                el.attrib[attr] = host + dirname(parsed_url.path) + link

        for el in htmltree.cssselect('img'):
            fix_attr(el, 'src')

        for el in htmltree.cssselect('a'):
            fix_attr(el, 'href')


class AlternateRss(models.Model):
    channel = models.ForeignKey(Channel, models.CASCADE)
    rss = models.CharField(max_length=250)

    def __str__(self):
        return self.rss


class Automation(models.Model):
    newspaper = models.ForeignKey('articles.Newspaper', models.CASCADE)

    def __str__(self):
        return get_newspaper_full_name(self.newspaper_id)


class AutomationItem(models.Model):
    NEWSPAPER = 'newspaper'
    TWEET = 'tweet'

    KIND_CHOICES = (
        (NEWSPAPER, _('Newspaper')),
        (TWEET, _('Tweet')),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    kind = models.CharField(max_length=60, choices=KIND_CHOICES, blank=True, null=True)
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE)

    def __str__(self):
        if self.kind:
            return f"{self.author.username}/{self.kind}"
        else:
            return self.author.username


@receiver(post_publish)
def on_post_published(sender, post, **kwargs):
    q = Automation.objects.filter(
        Q(automationitem__kind__isnull=True) | Q(automationitem__kind=post.kind),
        automationitem__author=post.author,
    )
    for automation in q:
        Backlog.objects.create(
            newspaper_id=automation.newspaper_id,
            post=post,
            publish_in=Backlog.UPCOMING_ISSUE,
        )
