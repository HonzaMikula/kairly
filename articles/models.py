from django.db import models

from django.utils.translation import ugettext_lazy as _


class Post(models.Model):

    NEWSPAPER = 'newspaper'
    TWEET = 'tweet'
    PICTURE = 'picture'

    KIND_CHOICES = (
        (NEWSPAPER, _('Newspaper')),
        (TWEET, _('Tweet')),
        (PICTURE, _('Picture')),
    )

    kind = models.CharField(max_length=60, choices=KIND_CHOICES, default=NEWSPAPER)
    published = models.DateTimeField(_('Published'), auto_now_add=True)
    title = models.CharField(max_length=160)
    perex = models.TextField(_("Content"), blank=True, null=True)
    content = models.TextField(_("Content"))
    is_draft = models.BooleanField(default=True, db_index=True)
    author = models.ForeignKey('users.User', models.PROTECT)

    def __str__(self):
        return self.title


class Edition(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField()
    published = models.DateTimeField(_('Published'), auto_now_add=True)
    user = models.ForeignKey('users.User', models.PROTECT, related_name='editions')
    editor = models.ForeignKey('users.User', models.PROTECT, related_name='+')
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.title
