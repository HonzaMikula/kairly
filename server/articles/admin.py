from django.contrib import admin

from .models import Newspaper


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'kind', 'author', 'draft', 'published', 'read_time')
#     list_filter = ('kind', 'draft')
#     exclude = ('guid',)
#     readonly_fields = ('source',)
#     search_fields = ('title', 'author__name', 'author__username')


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'editor', 'slug', 'price_int', 'period', 'period_time', 'period_dow', 'description')

    def price_int(self, obj):
        return int(obj.price)
    price_int.short_description = 'Price'
    price_int.admin_order_field = 'price'

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (returns None in that case).
        """
        if db_field.name == 'editor':
            manager = db_field.remote_field.model._default_manager
            try:
                newspaper_id = int(request.resolver_match.kwargs['object_id'])
            except KeyError:
                newspaper_id = None

            if newspaper_id:
                newspaper = Newspaper.objects.get(id=newspaper_id)
                if newspaper.editor_id:
                    return manager.filter(id=newspaper.editor_id)
            return manager.all()[:250]

        super().get_field_queryset(db, db_field, request)
