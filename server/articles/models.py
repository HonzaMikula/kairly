import rapidjson as json
import math
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import re
import hashlib

from bs4 import BeautifulSoup
import pytz

from django.conf import settings
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from utils.json import datetime_isoformat_ecma262
from utils.url import clean_url
from .period import PeriodMixin, periodicity_to_json
from .weight import calculate_post_weight


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
    TWEET = 'tweet'
    RECOMMENDATION = 'recommendation'
    LINK = 'link'

    KIND_CHOICES = (
        (NEWSPAPER, _('Newspaper')),
        (TWEET, _('Tweet')),
        (RECOMMENDATION, _('Recommendation')),
        (LINK, _('Link')),
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
        for p in cls.objects.filter(source_md5=md5).order_by('-published'):
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
        author_price = self.author.price
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

    def to_json(self, short=False, anonymous=False, tzinfo=timezone.utc):
        result = {
            'id': self.id,  # id is still used by backlog endpoints, TODO remove this
            'slug': self.slug,
            'author': self.author.to_json(),
            'source': self.source,
            'type': self.kind,
            'time': datetime_isoformat_ecma262(self.published.astimezone(tzinfo)),
            'price': None if self.price is None else str(self.price),
        }
        if self.draft:
            result['draft'] = True

        if self.kind == Post.TWEET:
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
        elif self.kind == Post.RECOMMENDATION:
            if self.ref_post:
                result['type'] += '-post'
                result['ref'] = self.ref_post.to_json(short, anonymous, tzinfo)
            else:
                result['type'] += '-issue'
                result['ref'] = self.ref_issue.to_json(tzinfo=tzinfo)
        elif self.kind == Post.LINK:
            result['content'] = {
                'title': self.title,
                'perex': self.perex,
            }
            if self.attachments:
                result['content']['attachments'] = json.loads(self.attachments)
        return result


class Newspaper(models.Model, PeriodMixin):
    title = models.CharField(max_length=160)
    slug = models.SlugField(_('Slug'))
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='editions', null=True, blank=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)
    price = models.DecimalField(_('Price'), max_digits=11, decimal_places=2,
                                default=Decimal(0),
                                validators=[MinValueValidator(Decimal(0))])

    period = models.CharField(max_length=32, choices=PeriodMixin.PERIOD_CHOICES, default=PeriodMixin.DAILY)
    period_time = models.TimeField(null=True, blank=True)  # time for daily and weekly period
    period_dow = models.IntegerField(null=True, blank=True)  # ISO week day for weekly period

    newsletter_subscription_url = models.CharField(_('Mailchimp subscribe form URL'), max_length=160, null=True, blank=True)

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

    def to_json(self, tzinfo):
        data = {
            "name": self.slug,
            "fullName": self.full_name,
            "title": self.title,
            "picture": settings.MEDIA_SITE + self.image.url if self.image else None,
            "description": self.description,
            "editor": self.editor.to_json(),
            "periodicity": periodicity_to_json(self),
            "nextRelease": datetime_isoformat_ecma262(self.next_release.astimezone(tzinfo)),
            "issues": self.issues,
            "likes": self.likes,
            "price": str(self.price),
        }
        if self.newsletter_subscription_url:
            data['newsletterSubscriptionUrl'] = self.newsletter_subscription_url
        return data


class Backlog(models.Model):
    newspaper = models.ForeignKey(Newspaper, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    publish_stamp = models.DateTimeField(_('Time when marked to publish'), null=True)
    ordering = models.IntegerField(null=True)

    @classmethod
    def consider_post(cls, newspaper, post):
        if cls.objects.filter(newspaper=newspaper, post=post).exists():
            return None

        return cls.objects.create(
            newspaper=newspaper,
            post=post
        )


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
            "newspaper": newspaper.to_json(tzinfo),  # TODO return newspapers separately, as done alredy for subscriptions
            "time": datetime_isoformat_ecma262(self.published.astimezone(tzinfo))
        }
        result['id'] = '{}/{}'.format(result['newspaper']['fullName'], self.number)
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
    suspended = models.BooleanField(default=False)
    donation = models.DecimalField(_('Donation'), max_digits=11, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return "Subscription to {}}".format(self.newspaper.full_name)

    def to_json(self):
        if self.suspended:
            state = 'suspended'
        elif self.renewal:
            state = 'active'
        else:
            state = 'canceled'

        data = {}
        data[self.newspaper.full_name] = {
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'state': state,
            'donation': str(self.donation) if self.donation != 0 else None,
        }
        return data


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

    def to_json(self):
        if self.suspended:
            state = 'suspended'
        elif self.renewal:
            state = 'active'
        else:
            state = 'canceled'

        author_json = self.author.to_json()
        data = {}
        data[author_json['id']] = {
            'author': author_json,  # is this needed?
            'periodicity': periodicity_to_json(self),
            'from': datetime_isoformat_ecma262(self.valid_from),
            'to': datetime_isoformat_ecma262(self.valid_to),
            'state': state,
            'donation': str(self.donation) if self.donation != 0 else None,
        }
        return data


@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache_key = Post.READ_TIME_CACHE_KEY.format(id=instance.id)
    cache.delete(cache_key)
