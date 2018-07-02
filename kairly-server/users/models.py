import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible

from articles.period import periodicity_to_json


@deconstructible
class KairlyUsernameValidator(validators.RegexValidator):
    regex = r'^([a-zA-Z0-9]+-)*[a-zA-Z0-9]+$'
    message = _(
        'Username may only contain alphanumeric characters or single hyphens, '
        'and cannot begin or end with a hyphen'
    )
    flags = re.ASCII

    min_length = 3
    reserved_names = [
        'login', 'logout', 'signin', 'signout',
        'signup', 'register', 'join', 'invite',
        'admin', 'home', 'pricing', 'welcome', 'timeline', 'about', 'help', 'settings',
        'site', 'page', 'app', 'post', 'action',
        'sites', 'pages', 'apps', 'posts', 'actions',
        'user', 'author', 'edition', 'profile', 'issue',
        'users', 'authors', 'editions', 'profiles', 'issues',
        'explore', 'dashboard', 'recent',
        'subscription', 'subscriptions',
        'join-and-read-with-kairly',
    ]

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError('Min length is {}'.format(self.min_length))
        if value in self.reserved_names:
            raise ValidationError('Username {} is reserved'.format(self.value))
        return super().__call__(value)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = KairlyUsernameValidator()

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

    medium = models.CharField(_("Medium"), max_length=160, blank=True)
    picture = models.ImageField(upload_to='users', null=True, blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    timezone = models.CharField(_("Timezone"), max_length=160, default="GMT")

    twitter_account = models.CharField(max_length=160, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def to_json(self, topic=None):
        id = self.username
        name = self.name or self.username
        if topic:
            id = '{}|{}'.format(id, topic.slug)
            name = '{} | {}'.format(name, topic.name)

        res = {
            'id': id,
            'name': name,
            'picture': self.picture.url if self.picture else '',
            'medium': self.medium,
            'bio': self.bio,
            'timezone': self.timezone,
            'integrations': {
                'twitter': self.twitter_account
            }
        }

        # TODO what about param (ma)
        if hasattr(self, 'user_subscription'):
            sub = self.user_subscription
            res['subscription'] = periodicity_to_json(sub) if sub else None

        return res
