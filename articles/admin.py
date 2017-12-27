from django.contrib import admin

from .models import Post, Edition


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    pass
