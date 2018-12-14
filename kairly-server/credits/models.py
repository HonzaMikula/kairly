from decimal import Decimal

from django.db import models, transaction
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from utils.json import datetime_isoformat_ecma262
from users.models import User
from articles.models import Newspaper


class Transaction(models.Model):
    AUTHOR_SUBSCRIPTION = 'AS'
    NEWSPAPER_SUBSCRIPTION = 'NS'
    DONATION = 'DO'
    FREE_CREDIT = 'FC'
    PLATFORM_FEE = 'PF'

    KIND_CHOICES = (
      (AUTHOR_SUBSCRIPTION, 'Author Subscription'),
      (NEWSPAPER_SUBSCRIPTION, 'Newspaper Subscription'),
      (DONATION, 'Donation'),
      (FREE_CREDIT, 'Free Credit'),
      (PLATFORM_FEE, 'Platform fee'),
    )

    from_platform = models.BooleanField(db_index=True, default=False)
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    from_author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    from_newspaper = models.ForeignKey(Newspaper, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    to_platform = models.BooleanField(db_index=True, default=False)
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    to_author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    to_newspaper = models.ForeignKey(Newspaper, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    kind = models.CharField(max_length=2, choices=KIND_CHOICES, db_index=True)
    credits = models.DecimalField(_('Credits'), max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_balance(cls, user):
        cache_key = f'balance_{user.id}'
        balance = cache.get(cache_key)
        if balance is None:
            expenses = cls.objects.filter(from_user=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
            income = cls.objects.filter(to_user=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
            balance = income - expenses
            cache.set(cache_key, str(balance))
        else:
            balance = Decimal(balance)
        return balance

    @classmethod
    def on_credits_change(cls, user):
        def clear_cache():
            cache.delete(f'balance_{user.id}')
        transaction.on_commit(clear_cache)

    def __str__(self):
        return '{} {}'.format(self.user.username, self.credits)

    def to_json(self):
        source = None
        if self.from_user:
            source = self.from_user.username
        elif self.from_author:
            source = self.from_author.username
        elif self.from_newspaper:
            source = self.from_newspaper.full_name
        target = None
        if self.to_user:
            target = self.to_user.username
        elif self.to_author:
            target = self.to_author.username
        elif self.to_newspaper:
            target = self.to_newspaper.full_name
        return {
            'source': source,
            'target': target,
            'kind': self.kind,
            'credits': str(self.credits),
            'created': datetime_isoformat_ecma262(self.created),
        }
