from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from .models import Channel, TwitterChannel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'author', 'topic', 'enabled', 'rss')

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
            path('<int:channel_id>/preview/<int:index>/', self.preview),
        ]
        return my_urls + urls

    def preview(self, request, channel_id, index):
        channel = Channel.objects.get(id=channel_id)

        entries = []
        for entry in channel.parse_rss().entries:
            if channel.is_url_valid(entry.link):
                entries.append(entry)

        try:
            entry = entries[index]
        except IndexError:
            context = dict(
               self.admin_site.each_context(request),
            )
            return TemplateResponse(request, "admin/preview-empty.html", context)

        perex, content = channel.parse_entry(entry)

        if len(entries) > index + 1:
            next_link = '/admin/sources/channel/{}/preview/{}/'.format(
                channel_id, index + 1)
        else:
            next_link = None

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           url=entry.link.split('#', maxsplit=1)[0],
           article_title=entry.title,
           perex=perex,
           content=content,
           next_link=next_link
        )
        return TemplateResponse(request, "admin/preview.html", context)


@admin.register(TwitterChannel)
class TwitterChannelAdmin(admin.ModelAdmin):
    list_display = ('twitter_account', 'author', 'topic', 'enabled')

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
                channel = TwitterChannel.objects.get(id=channel_id)
                if channel.author_id:
                    return manager.filter(author_id=channel.author_id)
            return manager.none()

        super().get_field_queryset(db, db_field, request)
