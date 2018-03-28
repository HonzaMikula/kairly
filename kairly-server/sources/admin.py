from django.contrib import admin

from .models import Channel


@admin.register(Channel)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'author', 'enabled', 'rss')
