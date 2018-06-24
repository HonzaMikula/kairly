import math
from datetime import timedelta, timezone

from bs4 import BeautifulSoup

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from .period import PeriodMixin


class Topic(models.Model):
    name = models.CharField(_("Name"), max_length=160)
    slug = models.SlugField(_('Slug'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, null=True)

    class Meta:
        unique_together = (("slug", "author"),)

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
    draft = models.BooleanField(_('Draft'), default=False)

    guid = models.CharField(_('External ID'), max_length=255, null=True, unique=True)
    source = models.CharField(_('Link to original article'), max_length=300, blank=True, null=True)

    title = models.CharField(max_length=160)
    picture = models.CharField(_("Picture"), max_length=300, blank=True, null=True)
    perex = RichTextField(_("Perex"), blank=True, null=True)
    content = RichTextField(_("Content"), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, null=True)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            for topic in self.topics.all():
                if topic.author_id != self.author_id:
                    raise ValueError("Topic auhtor doesn't match author")
        return super().save(*args, **kwargs)

    @property
    def read_time(self):
        if self.kind != Post.NEWSPAPER or not self.content:
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

    def to_json(self, short=False, tzinfo=timezone.utc):
        j = {
            'id': self.id,
            "author": self.author.to_json(),
            "type": self.kind,
            "time": str(self.published.astimezone(tzinfo)),
            "favorites": 131
        }
        if self.kind == Post.PICTURE:
            j['content'] = {
                'title': self.title,
                'picture': self.picture,
            }
        elif self.kind == Post.TWEET:
            j['content'] = {
                'content': self.content,
                'picture': self.picture,
            }
        elif self.kind == Post.NEWSPAPER:
            j['timeRead'] = self.read_time
            j['content'] = {
                'title': self.title,
                'content': self.perex if short else self.content,
                'perex': self.perex
            }
        return j


class Edition(models.Model, PeriodMixin):
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

    def to_json(self):
        result = {
            "id": "{}/{}".format(self.editor.username, self.slug),
            "title": self.title,
            "picture": settings.MEDIA_SITE + self.image.url,
            "description": self.description,
            "editor": self.editor.to_json(),
            "periodicity": {
                'frequency': self.period,
                'time': self.period_time,
                'dow': self.period_dow,
            },
            "issues": getattr(self, 'issues', 0),
            "likes": getattr(self, 'likes', 0)
        }
        if hasattr(self, 'user_subscription'):
            result['subscription'] = self.user_subscription is not None
        return result


class EditionBacklog(models.Model):
    edition = models.ForeignKey(Edition, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    publish_stamp = models.DateTimeField(_('Time when marked to publish'), null=True)


class EditionIssue(models.Model):
    number = models.IntegerField()
    published = models.DateTimeField(_('Published'), default=now)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)  # TODO why this is denormalized, why this is not taken from edition
    posts = models.ManyToManyField(Post, blank=True, through='EditionIssuePost')
    edition = models.ForeignKey(Edition, models.CASCADE)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return "{} #{}".format(self.edition.title, self.number)

    def to_json(self, posts=True, edition=None, tzinfo=timezone.utc):
        if edition is None:
            edition = self.edition
        result = {
            "number": self.number,
            "type": 'edition',
            "edition": {
                "id": "{}/{}".format(edition.editor.username, edition.slug),
                "title": edition.title,
                "periodicity": {
                    'frequency': edition.period,
                    'time': edition.period_time,
                    'dow': edition.period_dow,
                },
                "picture": settings.MEDIA_SITE + edition.image.url,
                "description": edition.description,
            },
            "time": str(self.published.astimezone(tzinfo)),
            "author": self.editor.to_json(),
        }
        if posts:
            result["posts"] = [
                p.to_json(short=True, tzinfo=tzinfo) for p in
                self.posts.all().order_by('editionissuepost__ordering', '-published')
            ]
        return result


class EditionIssuePost(models.Model):
    edition = models.ForeignKey(EditionIssue, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return self.post.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    edition = models.ForeignKey(Edition, models.CASCADE)

    class Meta:
        unique_together = (("user", "edition"),)


class SubscriptionToAuthor(models.Model, PeriodMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, related_name='+')
    topic = models.ForeignKey(Topic, models.CASCADE, blank=True, null=True)
    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True)  # ISO week day for weekly period

    class Meta:
        unique_together = (("user", "author", "topic"),)

    def save(self, *args, **kwargs):
        if self.topic and self.topic.author_id != self.author_id:
            raise ValueError("Topic doesn't match author")
        return super().save(*args, **kwargs)

    def get_issue_interval(self, dt):
        """Construct time interval which includes given datetime and matches
        period of author subscription.
        """
        # TODO move this to period module
        if self.period == SubscriptionToAuthor.X3_PER_DAY:
            if dt.hour < 6:
                return (
                    dt.replace(hour=18, minute=0, second=0, microsecond=0) - timedelta(days=1),
                    dt.replace(hour=6, minute=0, second=0, microsecond=0),
                    'Evening summary'
                )
            elif dt.hour >= 6 and dt.hour < 12:
                return (
                    dt.replace(hour=6, minute=0, second=0, microsecond=0),
                    dt.replace(hour=12, minute=0, second=0, microsecond=0),
                    'Morning summary'
                )
            elif dt.hour >= 12 and dt.hour < 18:
                return (
                    dt.replace(hour=12, minute=0, second=0, microsecond=0),
                    dt.replace(hour=18, minute=0, second=0, microsecond=0),
                    'Afternoon summary'
                )
            else:
                return (
                    dt.replace(hour=18, minute=0, second=0, microsecond=0),
                    dt.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1),
                    'Evening summary'
                )
        elif self.period == SubscriptionToAuthor.DAILY:
            sub_time = self.period_time
            start = dt.replace(hour=sub_time.hour, minute=sub_time.minute, second=0, microsecond=0)
            if start > dt:
                start -= timedelta(days=1)
            return start, start + timedelta(days=1), 'Daily summary'
        elif self.period == SubscriptionToAuthor.WEEKLY:
            sub_time = self.period_time
            start = dt.replace(hour=sub_time.hour, minute=sub_time.minute, second=0, microsecond=0)
            if start > dt:
                start -= timedelta(days=1)
            while start.isoweekday() != self.period_dow:
                start -= timedelta(days=1)
            return start, start + timedelta(days=7), 'Weekly summary'
        else:
            raise ValueError()


@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = Post.READ_TIME_CACHE_KEY.format(id=instance.id)
    cache.delete(cache_key)
