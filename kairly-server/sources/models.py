from os.path import dirname
from urllib.parse import urlsplit, urlunsplit
import codecs

import feedparser
import requests
import yaml
import lxml.html
from bs4 import UnicodeDammit

from django.db import models
from django.core.cache import cache
from django.conf import settings

from .parser import ArticleParser, split_article_to_perex_and_content


class Channel(models.Model):
    name = models.CharField(max_length=160)
    provider = models.CharField(max_length=32, help_text="Source identifier (namespace for guid)")
    rss = models.CharField(max_length=250)
    parse_content_from_rss = models.BooleanField(default=False)
    user_agent = models.CharField(help_text="Force User-Agent header when fetching RSS or post", max_length=250, null=True, blank=True)
    parser = models.TextField(help_text="Parse rules to get content from webpage/rss.", blank=False)
    skip_rules = models.TextField(help_text="YAML", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    topic = models.ForeignKey('articles.Topic', models.SET_NULL, blank=True, null=True, help_text="Save first with author to select a topic here.")
    newspaper = models.CharField(help_text="Automatically add to newspaper's backlog", max_length=160, null=True, blank=True, db_index=True)
    enabled = models.BooleanField(default=True)
    protected = models.BooleanField(default=True, help_text="Only users logged in can see full content")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # validate skip rules
        if self.skip_rules:
            yaml.load(self.skip_rules)

        if self.topic and self.topic.author_id != self.author_id:
            raise ValueError("Topic doesn't match author")

        if self.newspaper is not None and not self.newspaper.strip():
            self.newspaper = None

        super().save(*args, **kwargs)

    def parse_rss(self):
        kwargs = {}
        if self.user_agent:
            kwargs['agent'] = self.user_agent
        return feedparser.parse(self.rss, **kwargs)

    def parse_entry(self, entry, *, nocache=False):
        fragments = self.parse_article_from_entry(entry, nocache=nocache)
        perex, content = split_article_to_perex_and_content(fragments, 950)
        return perex, content

    def parse_article_from_entry(self, entry, *, nocache=False):
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
                html = entry.description
        else:
            html = self.fetch_url(url, nocache=nocache)

        htmltree = lxml.html.fromstring(html)
        try:
            # if descrption contains full html, dive into
            htmltree = htmltree.cssselect("body")[0]
        except IndexError:
            pass

        self.fix_relative_links(htmltree, parsed_url)
        parser = ArticleParser(self.parser)
        fragments = parser.parse(htmltree)
        fragments = parser.normalize(fragments)
        return fragments

    def fetch_url(self, url, *, nocache=False):
        cache_key = 'url-' + url
        html = None if nocache else cache.get(cache_key)
        if html is None:
            headers = {}
            if self.user_agent:
                headers['User-Agent'] = self.user_agent
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.encoding == 'ISO-8859-1':
                # some sources doesn't sent proper encoding header, eg osel.cz or atletika.cz
                encoding = self.get_encoding_From_meta(resp.content)
                if encoding is not None:
                    html = resp.content.decode(encoding)

                if html is None:
                    ud = UnicodeDammit(resp.content)
                    if ud.unicode_markup:
                        html = ud.unicode_markup

            if html is None:
                html = resp.content.decode(resp.encoding)
            cache.set(cache_key, html, 3600)
        return html

    def get_encoding_From_meta(self, content):
        for meta in lxml.html.fromstring(content).cssselect('meta'):
            try:
                if meta.attrib['http-equiv'] == 'Content-Type':
                    _, charset = meta.attrib['content'].split('=')
                    return codecs.lookup(charset).name
            except (KeyError, ValueError, LookupError):
                pass

    def is_url_valid(self, url):
        if not self.skip_rules:
            return True
        skip_rules = yaml.load(self.skip_rules)
        domain = skip_rules.get('domain')
        if domain:
            url = url.split('#', maxsplit=1)[0]
            return urlsplit(url).hostname != domain
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
