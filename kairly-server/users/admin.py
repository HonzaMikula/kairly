from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from dal import autocomplete

from .models import User, Category, CategoryUser

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'medium', 'picture', 'bio', 'timezone')}),
        (_('Integrations'), {'fields': ('twitter_account',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'img_picture', 'name', 'medium', 'is_active', 'timezone')
    search_fields = ('username', 'name', 'email')

    def img_picture(self, obj):
        if obj.picture:
            return mark_safe('<img src="{}" style="width: 32px; height: 32px; border-radius: 100%; object-fit: cover;" />'.format(obj.picture.url))
        else:
            return ''


class CategoryUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete')
    )

    class Meta:
        model = CategoryUser
        fields = ('user', 'topic', 'ordering')


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
