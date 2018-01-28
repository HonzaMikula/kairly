from django.contrib import admin

from .models import (Author, Post, EditionIssue, EditionIssuePost, Subscription,
                     UserSubscription)


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
    list_display = ('title', 'edition', 'editor', 'published', 'subscription')
    inlines = [
        PostInline,
    ]

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription')
