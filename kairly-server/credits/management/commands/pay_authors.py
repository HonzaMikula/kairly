import time
from datetime import timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

from credits.models import Transaction
from credits.utils import get_author_retained_credits, clear_credits_cache
from users.models import User


class Command(BaseCommand):
    help = 'Divide accumulated credits to user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            action='store',
            dest='month',
            help='Force month to assign (eg 12/2018)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry-run',
            help='do not create anything',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        dry_run = options.get('dry-run', False)

        counter_start = time.perf_counter()
        counter_total = Decimal(0)
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: pay authors started".format(timezone.now()))

        month = options.get('month')
        t = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if month:
            m, y = map(int, month.split('/'))
            t = t.replace(year=y, month=m)
            interval = (t, t + relativedelta(months=1))
        else:
            interval = (t - relativedelta(months=1), t)

        authors = Transaction.objects.filter(
            to_author__isnull=False,
            created__gte=interval[0],
            created__lt=interval[1],
        ).values_list('to_author', flat=True).distinct()

        for author_id in authors:
            credits = get_author_retained_credits(author_id, interval[1])
            if credits == 0:
                continue

            if verbosity > 0:
                username = User.objects.get(id=author_id).username
                self.stdout.write('Pay {} credits to author {}'.format(credits, username))

            counter_total += credits
            fee = (settings.CREDITS_FEE * credits).quantize(Decimal('.01'))
            user_credits = credits - fee

            with transaction.atomic():
                if not dry_run:
                    Transaction.objects.create(
                        from_author_id=author_id,
                        to_user_id=author_id,
                        credits=user_credits,
                        kind=Transaction.AUTHOR_SUBSCRIPTION
                    )
                    Transaction.objects.create(
                        from_author_id=author_id,
                        to_platform=True,
                        credits=fee,
                        kind=Transaction.AUTHOR_SUBSCRIPTION
                    )
                clear_credits_cache(user_id=author_id, author_id=author_id, platform=True)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: pay authors finished in {} / {} credits transfered".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_total))
