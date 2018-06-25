from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from .models import User


class UserAdmin(OriginalUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'medium', 'picture', 'bio', 'timezone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'img_picture', 'name', 'is_active', 'timezone')
    search_fields = ('username', 'name', 'email')

    def img_picture(self, obj):
        if obj.picture:
            return mark_safe('<img src="{}" style="width: 32px; height: 32px; border-radius: 100%; object-fit: cover;" />'.format(obj.picture))
        else:
            return ''


admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
