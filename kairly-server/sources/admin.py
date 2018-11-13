from urllib.parse import urlsplit, urlunsplit
from collections import namedtuple

import feedparser
import requests


from django.contrib import admin
from django.core.cache import cache
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path

from .models import Channel


FakeEntry = namedtuple('FakeEntry', ['link'])


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'author', 'newspaper', 'enabled', 'rss', 'parse_content_from_rss')
    list_filter = ('enabled', 'parse_content_from_rss')
    search_fields = ('name', 'provider', 'author__name')

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (returns None in that case).
        """
        if db_field.name == 'topic':
            manager = db_field.remote_field.model._default_manager
            try:
                channel_id = int(request.resolver_match.kwargs['object_id'])
            except KeyError:
                channel_id = None

            if channel_id:
                channel = Channel.objects.get(id=channel_id)
                if channel.author_id:
                    return manager.filter(author_id=channel.author_id)
            return manager.none()

        super().get_field_queryset(db, db_field, request)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:channel_id>/preview/', self.preview),
            path('<int:channel_id>/render-preview/', self.render_preview),
        ]
        return my_urls + urls

    def get_channel_feed(self, channel):
        cache_key = 'rss-' + channel.rss
        rss_content = cache.get(cache_key)
        if rss_content is None:
            headers = {}
            if channel.user_agent:
                headers['User-Agent'] = channel.user_agent

            resp = requests.get(channel.rss, headers=headers)
            resp.raise_for_status()

            rss_content = resp.text
            cache.set(cache_key, rss_content, 120)

        return feedparser.parse(rss_content)

    def preview(self, request, channel_id):
        channel = Channel.objects.get(id=channel_id)
        try:
            feed = self.get_channel_feed(channel)
        except requests.HTTPError as e:
            return TemplateResponse(request, "admin/preview-error.html", {"error": str(e)})

        rss_entries = []
        for entry in feed.entries:
            if channel.is_url_valid(entry.link):
                parsed_url = urlsplit(entry.link)
                url = urlunsplit(parsed_url[:-1] + ("",))  # strip fragment
                rss_entries.append({
                    'title': entry.title,
                    'link': url
                })

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           channel=channel,
           rss_entries=rss_entries
        )
        return TemplateResponse(request, "admin/preview.html", context)

    def render_preview(self, request, channel_id):
        url = request.POST['url']
        parser = request.POST['parser']

        channel = Channel.objects.get(id=channel_id)

        fake_channel = Channel(
            parser=parser,
            user_agent=channel.user_agent,
            parse_content_from_rss=channel.parse_content_from_rss
        )

        if channel.parse_content_from_rss:
            feed = self.get_channel_feed(channel)
            for feed_entry in feed.entries:
                if feed_entry.link.startswith(url):
                    entry = feed_entry
                    break
            else:
                return HttpResponse('Entry not found in RSS')
        else:
            entry = FakeEntry(url)
        perex, content = fake_channel.parse_entry(entry)

        document = ''.join([
            perex,
            '<div class="hr"><div>continue reading</div></div>',
            content,
        ])

        return HttpResponse(document)
