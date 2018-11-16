import time
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
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
        verbosity = options.get('verbosity')

        counter_start = time.perf_counter()
        counter_author = 0
        counter_newspaper = 0
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: renewsubscriptions started".format(timezone.now()))

        now = timezone.now() + timedelta(minutes=10)

        for sub in Subscription.objects.filter(valid_to__lt=now, renewal=True).select_related('user', 'newspaper'):
            if verbosity > 0:
                self.stdout.write('Extending newspaper subscription: {} -> {}'.format(sub.user, sub.newspaper.slug))

            counter_newspaper += 1
            self.extend_subscriptions(sub)

        for sub in SubscriptionToAuthor.objects.filter(valid_to__lt=now, renewal=True).select_related('user', 'author'):
            author_id = sub.author.username

            if verbosity > 1:
                self.stdout.write('Extending author subscription: {} -> {}'.format(sub.user, author_id))

            counter_author += 1
            self.extend_subscriptions(sub)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: renewsubscriptions finished in {} / extended subscriptions: {} author / {} newspaper".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_author, counter_newspaper))
