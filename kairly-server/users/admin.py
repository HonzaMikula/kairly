from datetime import timedelta

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.timezone import localdate

from dal import autocomplete

from .models import User, Category, CategoryUser

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
    list_display = ('username', 'email', 'img', 'name', 'kind', 'medium', 'price_int', 'is_active', 'last_logged', 'activity')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'kind')
    search_fields = ('username', 'name', 'email')

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


class CategoryUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete')
    )

    class Meta:
        model = CategoryUser
        fields = ('user', 'ordering')


class CategoryUserInline(admin.TabularInline):
    model = CategoryUser
    form = CategoryUserForm
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'explore_tab', 'ordering')
    search_fields = ('name',)

    inlines = [
        CategoryUserInline,
    ]
