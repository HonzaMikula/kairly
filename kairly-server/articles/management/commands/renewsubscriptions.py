from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now as timezone_now
from django.db import transaction

from articles.models import Subscription, SubscriptionToAuthor


class Command(BaseCommand):
    help = 'Extend subscriptions to be expired and marked for renew'

    @transaction.atomic
    def extend_subscriptions(self, sub):
        # TODO adjust date according to startdate
        # (if started on 31st, then end on 31st in moths which has 31 days, same with 29 and 30th)
        valid_to = sub.valid_to + relativedelta(months=1)
        sub.valid_to = valid_to
        sub.save()

    def handle(self, *args, **options):
        now = timezone_now() + timedelta(minutes=10)

        for sub in Subscription.objects.filter(valid_to__lt=now, renewal=True).select_related('user', 'newspaper'):
            self.stdout.write('Extending newspaper subscription: {} -> {}'.format(sub.user, sub.newspaper.slug))
            self.extend_subscriptions(sub)

        for sub in SubscriptionToAuthor.objects.filter(valid_to__lt=now, renewal=True).select_related('user', 'author'):
            if sub.topic:
                author_id = "{}|{}".format(sub.author.username, sub.topic.slug)
            else:
                author_id = sub.author.username
            self.stdout.write('Extending author subscription: {} -> {}'.format(sub.user, author_id))
            self.extend_subscriptions(sub)
