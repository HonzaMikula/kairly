from urllib.parse import urlparse

import feedparser
import requests
import yaml
import lxml.html
from lxml.etree import tostring

from django.db import models
from django.conf import settings

from .parser import ArticleParser


def flatten_tree(htmltree):
    childs = list(htmltree)
    if childs:
        for el in childs:
            if el.tag == 'div':
                yield from flatten_tree(el)
            else:
                yield el
    else:
        yield htmltree


class Channel(models.Model):
    name = models.CharField(max_length=160)
    provider = models.CharField(max_length=32, help_text="Source identifier (namespace for guid)")
    rss = models.CharField(max_length=250)
    parse_content_from_rss = models.BooleanField(default=False)
    parser = models.TextField(help_text="Parse rules to get content from webpage.", blank=True)
    skip_rules = models.TextField(help_text="YAML", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    topic = models.ForeignKey('articles.Topic', models.SET_NULL, blank=True, null=True, help_text="Save first with author to select a topic here.")
    enabled = models.BooleanField(default=True)

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

        super().save(*args, **kwargs)

    def parse_rss(self):
        return feedparser.parse(self.rss)

    def parse_entry(self, entry):
        article = self.parse_article_from_entry(entry)
        htmltree = lxml.html.fromstring(article)
        chars = 0
        perex = []
        nocontent = False
        for i, el in enumerate(flatten_tree(htmltree)):
            if el.tag == 'img':
                element_size = 180
            else:
                element_size = len(el.text_content())

            if perex and chars + element_size > 1600:
                break

            t = (el.tag, tostring(el, encoding='utf-8').decode('utf-8'))
            chars += element_size
            perex.append(t)
            el.getparent().remove(el)
        else:
            nocontent = True

        def is_hx(tag):
            return tag[0] == 'h' and len(tag) == 2

        while perex and is_hx(perex[-1][0]):
            perex.pop()

        perex = '\n\n'.join(p[1] for p in perex)
        content = '' if nocontent else tostring(htmltree, encoding='utf-8').decode('utf-8')
        return perex, content

    def parse_article_from_entry(self, entry):
        url = entry.link.split('#', maxsplit=1)[0]
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
            html = None
            if hasattr(entry, 'content'):
                for content in entry.content:
                    if content.type == 'text/html':
                        html = content.value
                        break
            if html is None:
                html = entry.description
        else:
            resp = requests.get(url)

            # hack, use utf-8 if meta with such value exists, needed at least for osel.cz
            # which sends bad encoding header from server
            if b"<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>" in resp.content:
                encoding = 'utf-8'
            else:
                encoding = resp.encoding

            html = resp.content.decode(encoding)

        htmltree = lxml.html.fromstring(html)
        try:
            # if descrption contains full html, dive into
            htmltree = htmltree.cssselect("body")[0]
        except IndexError:
            pass

        self.fix_images(htmltree, url)
        parser = ArticleParser(self.parser)
        return parser.parse(htmltree)

    def is_url_valid(self, url):
        if not self.skip_rules:
            return True
        skip_rules = yaml.load(self.skip_rules)
        domain = skip_rules.get('domain')
        if domain:
            url = url.split('#', maxsplit=1)[0]
            return urlparse(url).hostname != domain
        return True

    def fix_images(self, htmltree, url):
        host = '//' + urlparse(url).hostname
        for el in htmltree.cssselect('img'):
            src = el.attrib.get('src')
            if src and src.startswith('/') and not src.startswith('//'):
                el.attrib['src'] = host + el.attrib['src']
