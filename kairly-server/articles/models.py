import rapidjson as json
import math
from datetime import datetime, timezone
import re
import hashlib

from bs4 import BeautifulSoup
import pytz

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from utils.json import datetime_isoformat_ecma262
from .period import PeriodMixin, periodicity_to_json


class Topic(models.Model):
    name = models.CharField(_("Name"), max_length=160)
    slug = models.SlugField(_('Slug'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, null=True)

    class Meta:
        unique_together = (("slug", "author"),)

    def __str__(self):
        return "{}/{}".format(self.author.username, self.name)


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

    slug = models.SlugField(_('Slug'), max_length=190, null=True)
    kind = models.CharField(max_length=60, choices=KIND_CHOICES, default=NEWSPAPER)
    published = models.DateTimeField(_('Published'), default=timezone_now, db_index=True)
    draft = models.BooleanField(_('Draft'), default=False)

    guid = models.CharField(_('External ID'), max_length=255, null=True, unique=True)
    source = models.CharField(_('Link to original article'), max_length=300, blank=True, null=True)
    protected = models.BooleanField(default=True, help_text="Only users logged in can see full content")

    title = models.CharField(max_length=160)
    picture = models.CharField(_("Picture"), max_length=300, blank=True, null=True)
    perex = models.TextField(_("Perex"), blank=True, null=True)
    content = models.TextField(_("Content"), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, null=True)
    topics = models.ManyToManyField(Topic)
    attachments = models.TextField(null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            for topic in self.topics.all():
                if topic.author_id != self.author_id:
                    raise ValueError("Topic auhtor doesn't match author")

        if not self.slug and not self.draft:
            slug_words = []
            for part in re.split(r'[\?\.|\-]', self.title):
                words = part.split()
                if not slug_words or len(slug_words) < 5:
                    slug_words.extend(words)
            slug = slugify(' '.join(slug_words[:9])[:64])

            h = hashlib.sha1()
            h.update(datetime.now().isoformat().encode())
            h.update(self.title.encode())
            slug += '--' + h.hexdigest()[:9]

            self.slug = slug
        return super().save(*args, **kwargs)

    @property
    def read_time(self):
        if self.kind != Post.NEWSPAPER or not self.content:
            return None
        cache_key = Post.READ_TIME_CACHE_KEY.format(id=self.id)
        value = cache.get(cache_key)
        if value is None:
            soup = BeautifulSoup(self.content, "lxml")
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            words = len(text.split())
            value = math.ceil(words / 275)
            cache.set(cache_key, value, None)
        return '{} min'.format(max(1, value))

    def to_json(self, short=False, anonymous=False, tzinfo=timezone.utc):
        result = {
            'id': self.id,  # id is still used by backlog endpoints, TODO remove this
            'slug': self.slug,
            'author': self.author.to_json(),
            'source': self.source,
            'type': self.kind,
            'time': datetime_isoformat_ecma262(self.published.astimezone(tzinfo)),
        }
        if self.draft:
            result['draft'] = True

        if self.kind == Post.PICTURE:
            result['content'] = {
                'title': self.title,
                'picture': self.picture,
            }
        elif self.kind == Post.TWEET:
            result['content'] = {
                'content': self.content,
            }
            if self.attachments:
                result['content']['attachments'] = json.loads(self.attachments)
        elif self.kind == Post.NEWSPAPER:
            if anonymous and self.protected:
                result['timeRead'] = self.read_time
                result['content'] = {
                    'title': self.title,
                    'perex': self.perex,
                    'protected': True
                }
            else:
                result['timeRead'] = self.read_time
                result['content'] = {
                    'title': self.title,
                    'perex': self.perex,
                    'protected': False
                }
                if not short:
                    result['content']['content'] = self.content
        return result


class Newspaper(models.Model, PeriodMixin):
    title = models.CharField(max_length=160)
    slug = models.SlugField(_('Slug'))
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='editions', null=True)  # temporary allow null
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)

    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True)  # ISO week day for weekly period

    class Meta:
        unique_together = (("slug", "editor"),)

    def __str__(self):
        return self.title

    @property
    def issues(self):
        # TODO make db attribute from it
        if not hasattr(self, '_issues'):
            self._issues = Issue.objects.filter(newspaper=self).count()
        return self._issues

    @property
    def likes(self):
        # TODO cache it and probably rename
        if not hasattr(self, '_likes'):
            now = timezone_now()
            self._likes = Subscription.objects.filter(
                newspaper=self,
                valid_from__lte=now, valid_to__gt=now).count()
        return self._likes

    @property
    def next_release(self):
        editor_tz = pytz.timezone(self.editor.timezone)
        return self.get_period_interval(timezone_now(), editor_tz).end

    def to_json(self, tzinfo):
        return {
            "name": self.slug,
            "fullName": "{}/{}".format(self.editor.username, self.slug),
            "title": self.title,
            "picture": settings.MEDIA_SITE + self.image.url,
            "description": self.description,
            "editor": self.editor.to_json(),
            "periodicity": periodicity_to_json(self),
            "nextRelease": datetime_isoformat_ecma262(self.next_release.astimezone(tzinfo)),
            "issues": self.issues,
            "likes": self.likes
        }


class Backlog(models.Model):
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    publish_stamp = models.DateTimeField(_('Time when marked to publish'), null=True)
    ordering = models.IntegerField(null=True)


class Issue(models.Model):
    number = models.IntegerField()
    published = models.DateTimeField(_('Published'), default=timezone_now, db_index=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)  # TODO why this is denormalized, why this is not taken from newspaper
    posts = models.ManyToManyField(Post, blank=True, through='IssuePost')
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return "{} #{}".format(self.newspaper.title, self.number)

    def to_json(self, posts=True, newspaper=None, anonymous=False, tzinfo=timezone.utc):
        if newspaper is None:
            newspaper = self.newspaper
        result = {
            "number": self.number,
            "type": 'newspaper',
            "newspaper": newspaper.to_json(tzinfo),
            "time": datetime_isoformat_ecma262(self.published.astimezone(tzinfo))
        }
        if posts:
            result["posts"] = [
                p.to_json(short=True, anonymous=anonymous, tzinfo=tzinfo) for p in
                self.posts.filter(draft=False, published__lt=timezone_now())
                    .order_by('issuepost__ordering', '-published')
            ]
        return result


class IssuePost(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return self.post.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    renewal = models.BooleanField(default=True)

    class Meta:
        unique_together = (("user", "newspaper"),)

    def __str__(self):
        return "Subscription to {}/{}".format(self.newspaper.editor.username, self.newspaper.slug)

    def to_json(self):
        full_name = "{}/{}".format(self.newspaper.editor.username, self.newspaper.slug)
        data = {}
        data[full_name] = {
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'renewal': self.renewal
        }
        return data


class SubscriptionToAuthor(models.Model, PeriodMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, related_name='+')
    topic = models.ForeignKey(Topic, models.CASCADE, blank=True, null=True)
    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True)  # ISO week day for weekly period
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    renewal = models.BooleanField(default=True)

    class Meta:
        unique_together = (("user", "author", "topic"),)

    def __str__(self):
        title = self.author.username
        if self.topic:
            title += '|' + self.topic.name
        return "SubscriptionToAuthor to {}".format(title)

    def save(self, *args, **kwargs):
        if self.topic and self.topic.author_id != self.author_id:
            raise ValueError("Topic doesn't match author")
        return super().save(*args, **kwargs)

    def to_json(self):
        author_json = self.author.to_json(topic=self.topic)
        data = {}
        data[author_json['id']] = {
            'author': author_json,  # is this needed?
            'periodicity': periodicity_to_json(self),
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'renewal': self.renewal
        }
        return data


@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = Post.READ_TIME_CACHE_KEY.format(id=instance.id)
    cache.delete(cache_key)
