import re
import time
import dateutil.parser
from urllib.parse import urlparse

import yaml
import requests
import lxml.html
from lxml.etree import tostring

from django.core.management.base import BaseCommand

from articles.models import Post
from sources.models import Channel


class Command(BaseCommand):
    help = 'Import posts from RSS channels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            action='store',
            dest='provider',
            help='Import just selected provider',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Override existing posts',
        )
        parser.add_argument(
            '--draft',
            action='store_true',
            dest='draft',
            help='Create posts as draft',
        )

    def cssselect_with_slice(self, htmltree, selector):
        m = re.search(r"\[(\d*)(:)?(\d*)\]$", selector)
        sl = None
        if m:
            selector = selector[:m.start()]
            b1 = int(m.group(1)) if m.group(1) else None
            b2 = int(m.group(3)) if m.group(3) else None
            if m.group(2) == ':':
                sl = slice(b1, b2)
            else:
                sl = slice(b1, b1 + 1)
        elements = htmltree.cssselect(selector)
        if sl:
            return elements[sl]
        return elements

    def fix_images(self, htmltree, url):
        host = '//' + urlparse(url).hostname
        for el in htmltree.cssselect('img'):
            src = el.attrib.get('src')
            if src and src.startswith('/') and not src.startswith('//'):
                el.attrib['src'] = host + el.attrib['src']

    def parse_document(self, selectors, htmltree):
        if not isinstance(selectors, list):
            selectors = [selectors]
        result = []
        for selector in selectors:
            if isinstance(selector, dict):
                keys = list(selector.keys())
                assert len(keys) == 1, keys
                wrap_into = keys[0]
                selector = selector[wrap_into]
            else:
                wrap_into = None
            for el in self.cssselect_with_slice(htmltree, selector):
                if wrap_into == 'img':
                    result.append('<img alt="{alt}" title="{title}" src="{src}" />'.format(
                        alt=el.attrib.get('alt'),
                        title=el.attrib.get('title'),
                        src=el.attrib.get('src')))
                else:
                    # content = el.text_content().strip()
                    content = tostring(el, encoding='utf-8').decode('utf-8')
                    if wrap_into:
                        result.append("<{tag}>{content}</{tag}>".format(tag=wrap_into, content=content))
                    else:
                        result.append(content)
        return '\n\n'.join(result)

    def parse_remainder(self, selectors, htmltree):
        if not isinstance(selectors, list):
            selectors = [selectors]
        for selector in selectors:
            if isinstance(selector, dict):
                selector = selector.values()[0]
            for el in self.cssselect_with_slice(htmltree, selector):
                el.getparent().remove(el)
        return tostring(htmltree, encoding='utf-8').decode('utf-8')

    def is_valid(self, url, skip_rules):
        domain = skip_rules.get('domain')
        if domain and urlparse(url).hostname == domain:
            return False
        return True

    def handle(self, *args, **options):
        channels = Channel.objects.filter(enabled=True).exclude(author__isnull=True)
        if options.get('provider'):
            channels = channels.filter(provider=options['provider'])

        for channel in channels:
            self.stdout.write('Fetching {}'.format(channel.rss))
            parsing_rules = yaml.load(channel.parsing_rules)
            skip_rules = parsing_rules.get('skip', {})

            for entry in channel.parse_rss().entries:
                guid = "{}|{}".format(channel.provider, entry.id)
                url = entry.link.split('#', maxsplit=1)[0]
                update = False

                if not self.is_valid(url, skip_rules):
                    continue

                if Post.objects.filter(guid=guid).exists():
                    if options.get('force'):
                        update = True
                    else:
                        self.stdout.write('Skipping {}. Already imported'.format(url))
                        continue

                if channel.parse_content_from_rss:
                    if hasattr(entry, 'content'):
                        htmltree = lxml.html.fromstring(entry.content[0].value)
                    else:
                        htmltree = lxml.html.fromstring(entry.description)

                else:
                    resp = requests.get(url)
                    resp_content = resp.content.decode(resp.encoding)
                    htmltree = lxml.html.fromstring(resp_content)

                self.fix_images(htmltree, url)
                perex = self.parse_document(parsing_rules['perex'], htmltree)

                if parsing_rules['content'] == '*':
                    assert channel.parse_content_from_rss
                    # ! parse_reminder is modifying html tree !
                    content = self.parse_remainder(parsing_rules['perex'], htmltree)
                else:
                    content = self.parse_document(parsing_rules['content'], htmltree)

                args = dict(
                    kind=Post.NEWSPAPER,
                    published=dateutil.parser.parse(entry.published),
                    draft=options.get('draft'),
                    guid=guid,
                    source=url,
                    title=entry.title,
                    perex=perex,
                    content=content,
                    author=channel.author
                )

                if update:
                    post = Post.objects.get(guid=guid)
                    post.__dict__.update(args)
                    post.save()
                else:
                    Post.objects.create(**args)

                self.stdout.write('Imported {}'.format(url))
                time.sleep(0.1)
