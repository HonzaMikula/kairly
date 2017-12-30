from django.contrib import admin

from .models import Post, Edition, UserEdition


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'author', 'published')


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'edition', 'editor', 'published')
    filter_horizontal = ('posts',)


@admin.register(UserEdition)
class UserEditionAdmin(admin.ModelAdmin):
    list_display = ('edition', 'user')
