import math

from bs4 import BeautifulSoup

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=160)
    medium = models.CharField(_("Medium"), max_length=160, blank=True)
    picture = models.CharField(_("Picture"), max_length=300)
    bio = models.TextField(_("Bio"), blank=True)

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

    READ_TIME_CACHE_KEY = 'read_time_{id}'

    class Meta:
        ordering = ('-published',)

    kind = models.CharField(max_length=60, choices=KIND_CHOICES, default=NEWSPAPER)
    published = models.DateTimeField(_('Published'), default=now)

    title = models.CharField(max_length=160)
    picture = models.CharField(_("Picture"), max_length=300, blank=True, null=True)
    perex = RichTextField(_("Perex"), blank=True, null=True)
    content = RichTextField(_("Content"), blank=True, null=True)
    author = models.ForeignKey(Author, models.PROTECT)

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        if self.kind != Post.NEWSPAPER:
            return None
        cache_key = Post.READ_TIME_CACHE_KEY.format(id=self.id)
        value = cache.get(cache_key)
        if value is None:
            soup = BeautifulSoup(self.content)
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            words = len(text.split())
            value = math.ceil(words / 275)
            cache.set(cache_key, value, None)
        return '{} min'.format(value)


class Subscription(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    editor = models.ForeignKey(Author, models.PROTECT)

    def __str__(self):
        return self.title


class EditionIssue(models.Model):
    title = models.CharField(max_length=160)
    edition = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    published = models.DateTimeField(_('Published'), default=now)
    editor = models.ForeignKey(Author, models.PROTECT, related_name='+')
    posts = models.ManyToManyField(Post, blank=True, through='EditionIssuePost')
    subscription = models.ForeignKey(Subscription, models.SET_NULL, null=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


class EditionIssuePost(models.Model):
    edition = models.ForeignKey(EditionIssue, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return self.post.title


class UserSubscription(models.Model):
    user = models.ForeignKey('auth.User', models.CASCADE)
    subscription = models.ForeignKey(Subscription, models.CASCADE)


@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = Post.READ_TIME_CACHE_KEY.format(id=instance.id)
    cache.delete(cache_key)
