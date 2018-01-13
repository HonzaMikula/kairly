from django.contrib import admin

from .models import Author, Post, Edition, UserTags


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'medium')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'author', 'published')


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'edition', 'editor', 'published', 'tag_list')
    filter_horizontal = ('posts',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(UserTags)
class UserTagsAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag_list')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
