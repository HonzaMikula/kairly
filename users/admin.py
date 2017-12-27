from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm, UsernameField
)
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User


class UserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'title', 'icon_link',
            'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser',
        )
        field_classes = {'username': UsernameField}


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('title', 'icon_link', 'first_name',
                                         'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2'),
    #     }),
    # )


admin.site.unregister(Group)
