from django.contrib import admin

from .models import (Author, Post, EditionIssue, EditionIssuePost, Edition,
                     Subscription)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'medium')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'medium')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'author', 'draft', 'published', 'read_time')
    exclude = ('guid',)
    readonly_fields = ('source',)
    search_fields = ('title',)


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
    list_display = ('title', 'slug', 'period', 'description')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'edition')
