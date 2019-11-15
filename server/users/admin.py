from datetime import timedelta

from django.db.models import Count, Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.timezone import localdate, now as timezone_now

from .models import User, ExploreTimeline
from articles.models import Subscription
from credits.utils import get_author_retained_credits, get_user_credits

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'kind', 'medium', 'picture', 'bio', 'timezone')}),
        (_('Integrations'), {'fields': ('twitter_account',)}),
        (_('Pricing'), {'fields': ('price',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'img', 'name', 'kind', 'medium', 'price_int', 'is_active', 'last_logged',
                    '_subscribed_newspapers', '_subscribed_authors', 'activity')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'kind')
    search_fields = ('username', 'name', 'email')

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        now = timezone_now()
        # unfortunatelly both subscriptions can't be annotated, probably Django bug
        # https://code.djangoproject.com/ticket/30518#ticket

        # return qs.annotate(
        #     subscribed_newspapers=Count('subscription', filter=Q(subscription__valid_to__gt=now) | Q(subscription__renewal=True))
        return qs.annotate(
            subscribed_authors=Count('subscriptiontoauthor', filter=Q(subscriptiontoauthor__valid_to__gt=now) | Q(subscriptiontoauthor__renewal=True))
        )

    def _subscribed_newspapers(self, obj):
        if obj.kind != User.PERSONAL:
            return '-'
        # return obj.subscribed_newspapers
        now = timezone_now()
        return Subscription.objects.filter(user=obj).filter(Q(valid_to__gt=now) | Q(renewal=True)).count()
    _subscribed_newspapers.short_description = 's/newspapers'
    # _subscribed_newspapers.admin_order_field = 'subscribed_newspapers'

    def _subscribed_authors(self, obj):
        if obj.kind != User.PERSONAL:
            return '-'
        return obj.subscribed_authors
    _subscribed_authors.short_description = 's/authors'
    _subscribed_authors.admin_order_field = 'subscribed_authors'

    def price_int(self, obj):
        return int(obj.price)
    price_int.short_description = 'Price'
    price_int.admin_order_field = 'price'

    def img(self, obj):
        if obj.picture:
            return mark_safe('<img src="{}" style="width: 32px; height: 32px; border-radius: 100%; object-fit: cover;" />'.format(obj.picture_url))
        else:
            return ''

    def last_logged(self, obj):
        return obj.activity_history_start
    last_logged.admin_order_field = 'activity_history_start'

    def activity(self, obj):
        content = []
        d = localdate()
        start = obj.activity_history_start
        history = obj.activity_history
        x = 60 * 3
        for i in range(60):
            if start < d:
                active = False
            else:
                active = history & 1
                history >>= 1

            d -= timedelta(days=1)
            x -= 3
            if i % 2:
                fill = '#0c0' if active else 'white'
            else:
                fill = '#0c0' if active else '#f9f9f9'
            content.append('<rect x="{}" y="0" width="3" height="25" fill="{}"><title>{}</title></rect>'.format(x, fill, d))

        return mark_safe(
            '<svg version="1.1" width="180" height="25" xmlns="http://www.w3.org/2000/svg">' +
            ''.join(content) +
            '</svg>'
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            extra_context['user_credits'] = get_user_credits(object_id)
            extra_context['author_credits'] = get_author_retained_credits(object_id)

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


@admin.register(ExploreTimeline)
class ExploreTimelineAdmin(admin.ModelAdmin):
    list_display = ('slug', )
    search_fields = ('slug',)
