from django.contrib import admin

from .models import (Author, Post, EditionIssue, EditionIssuePost, Edition,
                     Subscription)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'medium')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'author', 'published', 'read_time')


class PostInline(admin.TabularInline):
    model = EditionIssuePost


@admin.register(EditionIssue)
class EditionIssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'editor', 'published', 'edition')
    inlines = [
        PostInline,
    ]

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'period', 'description')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'edition')
