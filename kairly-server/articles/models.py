from django.db import models

from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=160)
    picture = models.CharField(_("Picture"), max_length=300)
    medium = models.CharField(_("Medium"), max_length=160)
    content = models.TextField(_("Content"))

    def __str__(self):
        return self.name


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
    read_time = models.CharField(max_length=160)

    title = models.CharField(max_length=160)
    picture = models.CharField(_("Picture"), max_length=300)
    perex = models.TextField(_("Perex"), blank=True, null=True)
    content = models.TextField(_("Content"))
    author = models.ForeignKey(Author, models.PROTECT)

    def __str__(self):
        return self.title

    @property
    def template(self):
        return f"articles/post/{self.kind}.html"


class Edition(models.Model):
    title = models.CharField(max_length=160)
    edition = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    published = models.DateTimeField(_('Published'), auto_now_add=True)
    editor = models.ForeignKey(Author, models.PROTECT, related_name='+')
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.title


class UserEdition(models.Model):
    edition = models.ForeignKey(Edition, models.CASCADE)
    user = models.ForeignKey('auth.User', models.CASCADE)
