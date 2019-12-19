from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from articles.models import Newspaper, get_newspaper_full_name
from users.models import User
from utils.json import datetime_isoformat_ecma262


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
    credits = models.DecimalField(_('Credits'), max_digits=11, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def to_json(self, entities, reversed=False):
        source = {}
        if self.from_user_id:
            entities.add(User, self.from_user)
            source['user'] = self.from_user.username
        elif self.from_author_id:
            entities.add(User, self.from_author)
            source['author'] = self.from_author.username
        elif self.from_newspaper_id:
            entities.add(Newspaper, self.from_newspaper_id)
            source['newspaper'] = get_newspaper_full_name(self.from_newspaper_id)

        target = {}
        if self.to_user_id:
            entities.add(User, self.to_user)
            target['user'] = self.to_user.username
        elif self.to_author_id:
            entities.add(User, self.to_author)
            target['author'] = self.to_author.username
        elif self.to_newspaper_id:
            entities.add(Newspaper, self.to_newspaper_id)
            source['newspaper'] = get_newspaper_full_name(self.to_newspaper_id)

        return {
            'source': source,
            'target': target,
            'kind': self.kind,
            'credits': str(self.credits * -1 if reversed else self.credits),
            'created': datetime_isoformat_ecma262(self.created),
        }


@receiver(post_save, sender=User)
def update_stock(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            from_platform=True,
            to_user=instance,
            kind=Transaction.FREE_CREDIT,
            credits=350,
        )
