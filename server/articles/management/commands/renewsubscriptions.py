import time
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache

from articles.models import Subscription, SubscriptionToAuthor
from articles.views import SUBSCRIPTIONS_CACHE_KEY
from credits.utils import get_user_credits, pay_author_subscription, pay_newspaper_subscription


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

        cache_invalidate = []

        for sub in Subscription.objects.filter(valid_to__lt=now, renewal=True, suspended=False).select_related('user', 'newspaper').order_by('valid_from'):
            with transaction.atomic():
                credits = get_user_credits(sub.user.id)
                if credits < sub.newspaper.price + sub.donation:
                    if verbosity > 0:
                        self.stdout.write('Suspending newspaper subscription: {} -> {}'.format(sub.user, sub.newspaper.slug))
                    sub.suspended = True
                    sub.save()

                    cache_invalidate.append(SUBSCRIPTIONS_CACHE_KEY.format(sub.user.username))
                else:
                    if verbosity > 0:
                        self.stdout.write('Extending newspaper subscription: {} -> {}'.format(sub.user, sub.newspaper.slug))
                    pay_newspaper_subscription(sub)
                    counter_newspaper += 1
                    self.extend_subscriptions(sub)

        for sub in SubscriptionToAuthor.objects.filter(valid_to__lt=now, renewal=True, suspended=False).select_related('user', 'author').order_by('valid_from'):
            author_id = sub.author.username

            with transaction.atomic():
                credits = get_user_credits(sub.user.id)
                if credits < sub.author.price + sub.donation:
                    if verbosity > 1:
                        self.stdout.write('Suspending author subscription: {} -> {}'.format(sub.user, author_id))
                    sub.suspended = True
                    sub.save()

                    cache_invalidate.append(SUBSCRIPTIONS_CACHE_KEY.format(sub.user.username))
                else:
                    if verbosity > 1:
                        self.stdout.write('Extending author subscription: {} -> {}'.format(sub.user, author_id))
                    pay_author_subscription(sub)
                    counter_author += 1
                    self.extend_subscriptions(sub)

        if cache_invalidate:
            cache.delete_many(cache_invalidate)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: renewsubscriptions finished in {} / extended subscriptions: {} author / {} newspaper".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_author, counter_newspaper))
