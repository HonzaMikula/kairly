import re
import pytz
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class KairlyUsernameValidator(validators.RegexValidator):
    regex = r'^([a-zA-Z0-9]+-)*[a-zA-Z0-9]+$'
    message = _(
        'Username may only contain alphanumeric characters or single hyphens, '
        'and cannot begin or end with a hyphen'
    )
    flags = re.ASCII

    min_length = 3
    reserved_names = {
        'login', 'logout', 'signin', 'signout',
        'signup', 'register', 'join', 'invite',
        'home', 'homepage', 'index', 'welcome', 'tutorial',
        'admin', 'pricing', 'timeline', 'about', 'help', 'settings',
        'site', 'page', 'app', 'post', 'action',
        'sites', 'pages', 'apps', 'posts', 'actions',
        'user', 'author', 'editor', 'edition', 'profile', 'issue', "newspaper",
        'users', 'authors', 'editors', 'editions', 'profiles', 'issues', "newspapers",
        'journalists', 'readers', 'publishers', 'think-tanks',
        'explore', 'dashboard', 'recent',
        'subscription', 'subscriptions',
        'join-and-read-with-kairly',
        'credits', 'transactions', 'orders', 'reports', 'reporting', 'terms',
        'platform', 'system', 'sys',
        'kairly'
    }

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError('Min length is {}'.format(self.min_length))
        if value in self.reserved_names:
            raise ValidationError('Username {} is reserved'.format(value))
        return super().__call__(value)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = KairlyUsernameValidator()

    PERSONAL = 'personal'
    MEDIUM = 'medium'

    KIND_CHOICES = (
        (PERSONAL, _('Personal')),
        (MEDIUM, _('Medium')),
    )

    username = models.CharField(
        _('username'),
        max_length=39,
        unique=True,
        help_text=_('Required. 39 chars max'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_('name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    kind = models.CharField(max_length=60, choices=KIND_CHOICES, default=PERSONAL)

    medium = models.CharField(_("Medium"), max_length=160, blank=True)
    picture = models.ImageField(upload_to='users', null=True, blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    timezone = models.CharField(_("Timezone"), max_length=160, default="GMT")

    price = models.DecimalField(_('Subscription price'), max_digits=11, decimal_places=2,
                                default=Decimal(0),
                                validators=[MinValueValidator(Decimal(0))])

    twitter_account = models.CharField(max_length=160, null=True, blank=True)

    activity_history = models.BigIntegerField(default=0)  # bit mask for days, starting from activity_history_start
    activity_history_start = models.DateField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def picture_url(self):
        if not self.picture:
            return ''
        value = str(self.picture)
        if value.startswith('http://') or value.startswith('https://'):
            return value
        return settings.MEDIA_SITE + self.picture.url

    @property
    def tzinfo(self):
        try:
            return pytz.timezone(self.timezone)
        except pytz.UnknownTimeZoneError:
            return pytz.timezone('GMT')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def to_json(self, owner=False):
        result = {
            'id': self.username,
            'name': self.name or self.username,
            'picture': self.picture_url,
            'kind': self.kind,
            'medium': self.medium,
            'bio': self.bio,
            "price": str(self.price),
        }

        if owner:
            result.update({
                'timezone': self.timezone,
                'integrations': {
                    'twitter': self.twitter_account
                }
            })
            if self.is_superuser:
                result['isAdmin'] = True

        return result


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=160)
    explore_tab = models.CharField(_("Explore Tab"), max_length=160)
    ordering = models.IntegerField(_("Ordering"))

    class Meta:
        ordering = ('explore_tab', 'ordering')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return '{} > {}'.format(self.explore_tab, self.name)


class CategoryUser(models.Model):
    category = models.ForeignKey(Category, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    ordering = models.IntegerField(_("Ordering"), default=999)

    class Meta:
        ordering = ('ordering',)
