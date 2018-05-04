from urllib.parse import urlparse

import feedparser
import requests
import yaml
import lxml.html
from lxml.etree import tostring

from django.db import models

from .parser import ArticleParser


class Channel(models.Model):
    name = models.CharField(max_length=160)
    provider = models.CharField(max_length=32, unique=True, help_text="Source identifier (namespace for guid)")
    rss = models.CharField(max_length=250)
    parse_content_from_rss = models.BooleanField(default=False)
    parsing_rules = models.TextField(help_text="YAML with perex and content keys")
    parser = models.TextField(help_text="Parse rules to get content from webpage.", blank=True)
    skip_rules = models.TextField(help_text="YAML", blank=True)
    author = models.ForeignKey('articles.Author', models.SET_NULL, blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # validate skip rules
        if self.skip_rules:
            yaml.load(self.skip_rules)
        super(Channel, self).save(*args, **kwargs)

    def parse_rss(self):
        return feedparser.parse(self.rss)

    def parse_entry(self, entry):
        article = self.parse_article_from_entry(entry)
        htmltree = lxml.html.fromstring(article)
        chars = 0
        perex = []
        nocontent = False
        for i, el in enumerate(htmltree):
            if el.tag == 'img':
                chars += 180
            else:
                chars += len(el.text_content())
            perex.append(tostring(el, encoding='utf-8').decode('utf-8'))
            el.getparent().remove(el)

            if chars >= 1200:
                break
        else:
            nocontent = True

        perex = '\n\n'.join(perex)
        content = '' if nocontent else tostring(htmltree, encoding='utf-8').decode('utf-8')
        return perex, content

    def parse_article_from_entry(self, entry):
        url = entry.link.split('#', maxsplit=1)[0]
        if self.parse_content_from_rss:
            if hasattr(entry, 'content'):
                html = entry.content[0].value
            else:
                html = entry.description
        else:
            resp = requests.get(url)
            html = resp.content.decode(resp.encoding)

        htmltree = lxml.html.fromstring(html)
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
