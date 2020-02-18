import hashlib
import math
import re
import traceback
from datetime import datetime, timedelta
from decimal import Decimal

import pytz
import orjson as json
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Count, Sum, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail

from .period import PeriodMixin, periodicity_to_json
from .weight import calculate_post_weight
from users.models import User
from utils.json import datetime_isoformat_ecma262, entities_key, Ref, MappedRef
from utils.url import clean_url


def round_fair_price(price):
    if price < 0.1:
        return Decimal('0.1')
    if price < 1:
        return price.quantize(Decimal('0.1'))
    if price < 5:
        # round to 0.5
        return (price * 2).quantize(Decimal(0)) / 2
    return price.quantize(Decimal(0))


class Post(models.Model):

    NEWSPAPER = 'newspaper'
    COMMENT = 'comment'  # eg issue intro, etc, no perex, just content
    TWEET = 'tweet'
    RECOMMENDATION = 'recommendation'
    LINK = 'link'
    VIDEO = 'video'

    KIND_CHOICES = (
        (NEWSPAPER, _('Newspaper')),
        (COMMENT, _('Comment')),
        (TWEET, _('Tweet')),
        (RECOMMENDATION, _('Recommendation')),
        (LINK, _('Link')),
        (VIDEO, _('Video')),
    )

    READ_TIME_CACHE_KEY = 'read_time_{id}'

    class Meta:
        ordering = ('-published',)

    slug = models.SlugField(_('Slug'), max_length=190, null=True)
    kind = models.CharField(max_length=60, choices=KIND_CHOICES, default=NEWSPAPER, db_index=True)
    published = models.DateTimeField(_('Published'), default=timezone_now, db_index=True)
    draft = models.BooleanField(_('Draft'), default=False)

    guid = models.CharField(_('External ID'), max_length=255, null=True, unique=True)
    source = models.CharField(_('Link to original article'), max_length=300, blank=True, null=True)  # be aware that utf8mb fields ca have index only if length <= 191
    source_md5 = models.CharField('Source MD5', max_length=32, blank=True, null=True, db_index=True)
    protected = models.BooleanField(default=True, help_text="Only users logged in can see full content")
    hidden = models.BooleanField(default=False, help_text="Don't show hidden posts in authors detail")

    title = models.CharField(max_length=160)
    perex = models.TextField(_("Perex"), blank=True, null=True)
    content = models.TextField(_("Content"), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, null=True)
    attachments = models.TextField(null=True)

    ref_post = models.ForeignKey('articles.Post', models.CASCADE, null=True)
    ref_issue = models.ForeignKey('articles.Issue', models.CASCADE, null=True)

    # pricing helpers
    price = models.DecimalField(
        _('Article price'), max_digits=11, decimal_places=2,
        null=True, validators=[MinValueValidator(Decimal(0))])
    weight = models.PositiveIntegerField(null=True)

    @classmethod
    def find_by_source_url(cls, url):
        url = clean_url(url)
        md5 = hashlib.md5(url.encode()).hexdigest()
        for p in cls.objects.filter(source_md5=md5).exclude(kind__in=[Post.LINK, Post.RECOMMENDATION]).order_by('-published'):
            if p.source == url:
                return p

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        recalculate_weight = kwargs.pop('recalculate_weight', False)

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

        if not self.draft and (recalculate_weight or self.weight is None):
            self.weight = calculate_post_weight(self)

        if not self.draft and self.price is None:
            self.price = self.calculate_fair_price()
            if self.price is None:
                self.price = round_fair_price(self.author.price / 5)

        if self.source and not self.source_md5:
            self.source_md5 = hashlib.md5(self.source.encode()).hexdigest()
        return super().save(*args, **kwargs)

    def calculate_fair_price(self):
        author_price = self.author.price if self.author else 0
        if author_price == 0:
            return Decimal(0)

        # compare only to articles to yesterday (this allows caching and easier rss imports)
        days = 30
        end = timezone_now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=days)

        cache_key = f"author_post_weight:{end:%Y%m%d}"
        cache_value = cache.get(cache_key)
        if cache_value:
            agg = json.loads(cache_value)
        else:
            agg = Post.objects.filter(author=self.author, draft=False, published__gte=start, published__lt=end) \
                              .exclude(kind=Post.RECOMMENDATION) \
                              .aggregate(count=Count('*'), weight=Sum('weight'))
            cache.set(cache_key, json.dumps(agg))

        count = agg['count']
        total_weight = agg['weight']

        if count == 0:
            return None

        if start < self.author.date_joined:
            # rare case for new author
            ratio = days / (start - self.author.date_joined).days
            total_weight = round(total_weight * ratio)

        post_weight = calculate_post_weight(self) if self.weight is None else self.weight

        total_weight += post_weight
        weight_fraction = min(0.5, post_weight / total_weight)

        return round_fair_price(Decimal(weight_fraction) * author_price)

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

    def to_json(self, entities, short=False):
        result = {
            'id': self.id,  # id is still used by backlog endpoints, TODO remove this
            'slug': self.slug,
            'source': self.source,
            'type': self.kind,
            'time': datetime_isoformat_ecma262(self.published.astimezone(entities.tzinfo)),
            'price': None if self.price is None else str(self.price),
        }
        if self.author_id:
            result['author'] = entities.make_ref(User, self.author_id)

        if self.draft:
            result['draft'] = True

        try:
            attachments = json.loads(self.attachments) if self.attachments else None
        except json.JSONDecodeError:
            print(f'Corrupted attachemnt for post id={self.id} slug={self.slug}')
            traceback.print_exc()
            attachments = None

        if self.kind == Post.TWEET:
            result['content'] = {
                'content': self.content,
            }
            if self.author_id is None and attachments:
                _attachments = []
                for a in attachments:
                    if a['type'] == 'author':
                        result['author'] = {
                           'id': 'twitter|' + a['screen_name'],
                           'name': a['name'],
                           'pictures': {
                               'small': a['profile_image_url_https']
                            },
                           'url': 'https://twitter.com/' + a['screen_name'],
                           'kind': 'external',
                        }
                    else:
                        _attachments.append(a)
                attachments = _attachments

            if attachments:
                result['content']['attachments'] = attachments
        elif self.kind == Post.VIDEO:
            result['content'] = {
                'title': self.title,
                'perex': self.perex,
                'protected': self.protected
            }
            if attachments:
                result['content']['attachments'] = attachments
        elif self.kind == Post.NEWSPAPER:
            if entities.user.is_anonymous and self.protected:
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
        elif self.kind == Post.COMMENT:
            result['content'] = {
                'title': self.title,
                'content': self.content,
            }
        elif self.kind == Post.RECOMMENDATION:
            if self.ref_post:
                result['type'] += '-post'
                result['ref'] = self.ref_post.to_json(entities, short)
            else:
                result['type'] += '-issue'
                result['ref'] = self.ref_issue.to_json(entities)
        elif self.kind == Post.LINK:
            result['content'] = {
                'title': self.title,
                'perex': self.perex,
            }
            if attachments:
                result['content']['attachments'] = attachments
        return result


# TODO DELETE
class Editorial(models.Model):
    ARTICLE = 'article'
    TWEETS = 'tweets'

    KIND_CHOICES = (
        (ARTICLE, _('Article')),
        (TWEETS, _('Tweets')),
    )

    title = models.CharField(max_length=160, null=True)
    content = models.TextField(_("Content"), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    kind = models.CharField(max_length=60, choices=KIND_CHOICES)
    position = models.CharField(max_length=32)

    def __str__(self):
        return self.title

    def to_json(self, entities):
        data = {
            'author': entities.make_ref(User, self.author_id),
            'type': self.kind,
            'position': self.position,
        }

        if self.kind == 'article':
            data['title'] = self.title
            data['content'] = self.content
        elif self.kind == 'tweets':
            tweets = EditorialTweet.objects.filter(editorial=self).select_related('post').order_by('ordering')
            data['tweets'] = [t.post.to_json(entities) for t in tweets]
        else:
            raise ValueError
        return data


# TODO DELETE
class EditorialTweet(models.Model):
    editorial = models.ForeignKey(Editorial, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    ordering = models.IntegerField(null=True)


@entities_key("newspapers", 1)
class Newspaper(models.Model, PeriodMixin):
    title = models.CharField(max_length=160)
    slug = models.SlugField(_('Slug'))
    description = models.TextField(blank=True)
    image = ImageField(upload_to='editions', null=True, blank=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)
    co_editors = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CoEditor", related_name="+")
    price = models.DecimalField(_('Price'), max_digits=11, decimal_places=2,
                                default=Decimal(0),
                                validators=[MinValueValidator(Decimal(0))])

    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True, blank=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True, blank=True)  # ISO week day for weekly period

    newsletter_subscription_url = models.CharField(_('Mailchimp subscribe form URL'), max_length=160, null=True, blank=True)
    archived = models.BooleanField(_('Archived'), default=False)

    class Meta:
        unique_together = (("slug", "editor"),)

    def __str__(self):
        return self.title

    @property
    def issues(self):
        # TODO what about making attribute from it or caching it
        if not hasattr(self, '_issues'):
            self._issues = Issue.objects.filter(newspaper=self).count()
        return self._issues

    @property
    def likes(self):
        # TODO what about making attribute from it or caching it
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

    def save(self, *args, **kwargs):
        transaction.on_commit(lambda: cache.delete(Ref(Newspaper, self.id).cache_key))
        return super().save(*args, **kwargs)

    def current_month_upcomming_issues(self):
        editor_tz = pytz.timezone(self.editor.timezone)
        dt = timezone_now().astimezone(editor_tz)
        month = dt.month
        issue_dates = []
        while True:
            dt = self.get_period_interval(dt, editor_tz).end
            if dt.month == month:
                issue_dates.append(dt)
            else:
                return issue_dates

    @property
    def full_name(self):
        return "{}/{}".format(self.editor.username, self.slug)

    def get_picture_url(self, size):
        if not self.image:
            return None

        value = str(self.image)
        if value.startswith('http://') or value.startswith('https://'):
            return value

        im = get_thumbnail(self.image, size, crop='center')
        if im:
            return settings.MEDIA_SITE + im.url
        else:
            return settings.MEDIA_SITE + self.image.url

    def to_json(self, entities):
        data = {
            "name": self.slug,
            "fullName": self.full_name,
            "title": self.title,
            "picture": self.get_picture_url('283x120'),
            "description": self.description,
            "editor": entities.make_ref(User, self.editor_id),
            "periodicity": periodicity_to_json(self),
            "issues": self.issues,
            "likes": self.likes,
            "price": str(self.price),
        }
        if entities.user.id == self.editor_id:
            data['coEditors'] = []
            for ce in self.co_editors.all().order_by('username'):
                data['coEditors'].append(entities.make_ref(User, ce.id))

        if self.newsletter_subscription_url:
            data['newsletterSubscriptionUrl'] = self.newsletter_subscription_url
        return data


class CoEditor(models.Model):
    """Keep relation as separate model because of future extension
    with different co-editor permissions
    """
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# TODO DELETE
class BacklogX(models.Model):
    UPCOMING_ISSUE = 1
    NEXT_ISSUE = 2

    newspaper = models.ForeignKey(Newspaper, models.CASCADE, db_constraint=False)
    post = models.ForeignKey(Post, models.CASCADE, db_constraint=False)
    publish_in = models.SmallIntegerField(null=True, db_index=True)
    ordering = models.IntegerField(null=True)
    editorial = models.ForeignKey(Editorial, models.SET_NULL, null=True, db_constraint=False)

    @classmethod
    def append_post(cls, newspaper, post):
        return cls._consider_post(newspaper, post, prepend=False)

    @classmethod
    def prepend_post(cls, newspaper, post):
        return cls._consider_post(newspaper, post, prepend=True)

    @classmethod
    def _consider_post(cls, newspaper, post, prepend):
        if isinstance(post, int):
            post_id = post
        else:
            post_id = post.id

        if cls.objects.filter(newspaper=newspaper, post_id=post_id).exists():
            return None

        if prepend:
            cls.objects.filter(newspaper=newspaper, publish_in__isnull=True).update(ordering=F('ordering') + 1)

        return cls.objects.create(
            newspaper=newspaper,
            post_id=post_id,
            ordering=0 if prepend else None
        )


class Backlog(models.Model):
    name = models.CharField(max_length=64)
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True, through='BacklogPost')
    layout = models.TextField(null=True)

    def to_json(self, entities):
        newspaper_ref = entities.make_ref(Newspaper, self.newspaper_id)
        result = {
            "name": self.name,
            "newspaper": newspaper_ref,
            "layout": json.loads(self.layout)
        }
        posts_json = {}
        for ip in BacklogPost.objects.filter(backlog=self).select_related('post'):
            posts_json[str(ip.post_id)] = ip.post.to_json(entities, short=True)
        result["posts"] = posts_json
        return result

    @classmethod
    def get_layout_posts(cls, layout):
        ids = set()
        for item in layout:
            if isinstance(item, list):
                ids.update(cls.get_layout_posts(item))
            elif isinstance(item, dict):
                post_id = item.get('post')
                if post_id:
                    ids.add(post_id)
        return ids


class BacklogPost(models.Model):
    backlog = models.ForeignKey(Backlog, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['backlog', 'post']]

    def __str__(self):
        return self.post.title


class Issue(models.Model):
    number = models.IntegerField()
    published = models.DateTimeField(_('Published'), default=timezone_now, db_index=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)  # TODO why this is denormalized, why this is not taken from newspaper
    posts = models.ManyToManyField(Post, blank=True, through='IssuePost')
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    layout = models.TextField(null=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return "{} #{}".format(self.newspaper.title, self.number)

    def to_json(self, entities, posts=True):
        newspaper_ref = entities.make_ref(Newspaper, self.newspaper_id)
        result = {
            "id": MappedRef(newspaper_ref, f'{{}}/{self.number}'),
            "number": self.number,
            "type": 'newspaper',
            "newspaper": newspaper_ref,
            "time": datetime_isoformat_ecma262(self.published.astimezone(entities.tzinfo)),
            "layout": json.loads(self.layout)
        }
        if posts:
            posts_json = []
            for ip in IssuePost.objects.filter(issue=self).select_related('post'):
                posts_json.append(ip.post.to_json(entities, short=True))
            result["posts"] = posts_json
        return result


class IssuePost(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    renewal = models.BooleanField(default=True)
    suspended = models.BooleanField(default=False)
    donation = models.DecimalField(_('Donation'), max_digits=11, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return f"Subscription to {self.newspaper_id}"

    def to_json(self, entities):
        if self.suspended:
            state = 'suspended'
        elif self.renewal:
            state = 'active'
        else:
            state = 'canceled'

        return {
            'newspaper': entities.make_ref(Newspaper, self.newspaper_id),
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'state': state,
            'donation': str(self.donation) if self.donation != 0 else None,
        }


class SubscriptionToAuthor(models.Model, PeriodMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, related_name='+')
    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True)  # ISO week day for weekly period
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    renewal = models.BooleanField(default=True)
    suspended = models.BooleanField(default=False)
    donation = models.DecimalField(_('Donation'), max_digits=11, decimal_places=2, default=Decimal(0))

    def __str__(self):
        title = self.author.username
        return "SubscriptionToAuthor to {}".format(title)

    def to_json(self, entities):
        if self.suspended:
            state = 'suspended'
        elif self.renewal:
            state = 'active'
        else:
            state = 'canceled'

        return {
            'author': entities.make_ref(User, self.author_id),
            'periodicity': periodicity_to_json(self),
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'state': state,
            'donation': str(self.donation) if self.donation != 0 else None,
        }


@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = Post.READ_TIME_CACHE_KEY.format(id=instance.id)
    cache.delete(cache_key)
