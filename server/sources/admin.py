from urllib.parse import urlsplit, urlunsplit
from collections import namedtuple

import feedparser
import requests

from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import escape, mark_safe
from django.db import transaction
from dal import autocomplete

from users.models import User
from articles.models import SubscriptionToAuthor, Post
from credits.models import Transaction
from .models import Channel, Automation, AutomationItem, AlternateRss

FakeEntry = namedtuple('FakeEntry', ['link'])


class AlternateRssItemInline(admin.TabularInline):
    model = AlternateRss
    extra = 1


class SelectChannelForm(forms.Form):
    channel = forms.ModelChoiceField(
        queryset=Channel.objects.filter(enabled=True),
        widget=autocomplete.ModelSelect2(url='channel-autocomplete')
    )


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
            path('<int:channel_id>/merge/', self.merge),
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

            resp = requests.get(channel.rss, headers=headers, verify=False)
            resp.raise_for_status()

            # strip whitespaces because eg. https://www.foliomag.com/feed/
            # generates invalid XML due to leading whitespaces
            rss_content = resp.text.strip()
            cache.set(cache_key, rss_content, 120)

        return feedparser.parse(rss_content)

    def merge(self, request, channel_id):
        channel = Channel.objects.get(id=channel_id)
        if not channel.author_id or channel.newspaper:
            raise ValueError("Only channel with author can be merged")

        if request.method == 'POST':
            form = SelectChannelForm(request.POST)
            if form.is_valid():
                target = form.cleaned_data['channel']
                if target == channel:
                    form.add_error("channel", "Can't merge into self")
                elif not target.author_id:
                    form.add_error("channel", "Channel has not author")
                else:
                    with transaction.atomic():
                        AlternateRss.objects.create(channel=target, rss=channel.rss)
                        SubscriptionToAuthor.objects.filter(author=channel.author).update(author=target.author)
                        Post.objects.filter(author=channel.author).delete()
                        Transaction.objects.filter(to_user=channel.author).delete()
                        channel.author.delete()
                        channel.delete()
                    return HttpResponseRedirect('/admin/sources/channel/')
        else:
            form = SelectChannelForm()

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            channel=channel,
            form=form
        )
        return TemplateResponse(request, "admin/merge.html", context)

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

        args = fake_channel.parse_entry(entry, usecache=True)

        document = ''.join([
            args['perex'],
            '<div class="hr"><div>continue reading</div></div>',
            args['content'],
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
