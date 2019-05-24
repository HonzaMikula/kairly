from urllib.parse import urlsplit, urlunsplit
from collections import namedtuple

import feedparser
import requests

from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import escape, mark_safe
from dal import autocomplete

from users.models import User
from .models import Channel, Automation, AutomationItem, AlternateRss


FakeEntry = namedtuple('FakeEntry', ['link'])


class AlternateRssItemInline(admin.TabularInline):
    model = AlternateRss
    extra = 1


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'author', 'newspaper', 'enabled', 'rss_all', 'import_links', 'parse_content_from_rss')
    list_filter = ('enabled', 'import_links', 'parse_content_from_rss')
    search_fields = ('name', 'provider', 'author__name', 'rss', 'alternaterss__rss')
    inlines = [AlternateRssItemInline]

    def get_queryset(self, request):
        return super(ChannelAdmin, self).get_queryset(request).prefetch_related('alternaterss_set')

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
            else:
                headers['User-Agent'] = settings.DEFAULT_USER_AGENT

            resp = requests.get(channel.rss, headers=headers)
            resp.raise_for_status()

            # strip whitespaces because eg. https://www.foliomag.com/feed/
            # generates invalid XML due to leading whitespaces
            rss_content = resp.text.strip()
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
        perex, content, _ = fake_channel.parse_entry(entry, usecache=True)

        document = ''.join([
            perex,
            '<div class="hr"><div>continue reading</div></div>',
            content,
        ])

        return HttpResponse(document)

    def rss_all(self, obj):
        rss_list = [escape(obj.rss)]
        rss_list.extend(escape(a.rss) for a in obj.alternaterss_set.all())
        return mark_safe('<br>'.join(rss_list))
    rss_all.admin_order_field = 'rss'
    rss_all.short_description = 'RSS'


class AutomationItemForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete')
    )

    class Meta:
        model = AutomationItem
        fields = ('author', 'kind')


class AutomationItemInline(admin.TabularInline):
    model = AutomationItem
    form = AutomationItemForm
    extra = 1


# class AutomationItemInline(admin.TabularInline):
#     model = AutomationItem
#     fields = ('author', 'kind')
#     extra = 1


@admin.register(Automation)
class AutomationAdmin(admin.ModelAdmin):
    inlines = [AutomationItemInline]
