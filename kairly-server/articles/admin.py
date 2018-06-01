from django.contrib import admin

from .models import (Author, Topic, Post, EditionIssue, EditionIssuePost,
                     Edition, Subscription)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'medium')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'medium')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'author', 'draft', 'published', 'read_time')
    exclude = ('guid',)
    readonly_fields = ('source',)
    search_fields = ('title',)

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (returns None in that case).
        """
        if db_field.name == 'topics':
            manager = db_field.remote_field.model._default_manager
            post_id = int(request.resolver_match.kwargs['object_id'])

            if post_id:
                post = Post.objects.get(id=post_id)
                if post.author_id:
                    return manager.filter(author_id=post.author_id)
            return manager.none()

        super().get_field_queryset(db, db_field, request)


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
