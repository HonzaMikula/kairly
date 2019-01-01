import time
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN
from collections import defaultdict
from functools import lru_cache

from dateutil.relativedelta import relativedelta

from django.db import transaction
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

from articles.models import Issue, Newspaper, Post
from credits.models import Transaction
from credits.utils import get_newspaper_retained_credits, clear_credits_cache
from users.models import User


class Command(BaseCommand):
    help = 'Divide accumulated credits to users'

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
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: pay editors started".format(timezone.now()))

        month = options.get('month')
        t = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if month:
            m, y = map(int, month.split('/'))
            t = t.replace(year=y, month=m)
            interval = (t, t + relativedelta(months=1))
        else:
            interval = (t - relativedelta(months=1), t)

        @lru_cache(maxsize=None)
        def get_author_total_weight(author_id):
            weight = Post.objects.filter(
                draft=False,
                published__gte=interval[0],
                published__lt=interval[1],
                author_id=author_id
            ).aggregate(Sum('weight'))['weight__sum'] or 0
            return weight

        newspapers = Transaction.objects.filter(
            to_newspaper__isnull=False,
            created__gte=interval[0],
            created__lt=interval[1],
        ).values_list('to_newspaper', flat=True).distinct()

        for newspaper_id in newspapers:
            credits = get_newspaper_retained_credits(newspaper_id, interval[1])
            if credits == 0:
                continue

            counter_total += credits
            newspaper = Newspaper.objects.get(id=newspaper_id)

            if verbosity > 0:
                self.stdout.write('* {} collected {} credits on subscription'.format(newspaper.title, credits))

            issues = Issue.objects.filter(
                newspaper=newspaper,
                published__gte=interval[0],
                published__lt=interval[1],
            )

            posts = Post.objects.filter(issuepost__issue__in=issues, author_price__gt=0)

            author_cost = defaultdict(Decimal)
            total = 0

            for post in posts:
                post_cost = post.author_price * Decimal(post.weight) / Decimal(get_author_total_weight(post.author_id))
                author_cost[post.author_id] += post_cost
                total += post_cost

            remainder = credits
            with transaction.atomic():
                factor = max(total, newspaper.price)
                inv_fee = Decimal(1) - settings.CREDITS_FEE
                for author_id, cost in author_cost.items():
                    # self.stdout.write('{} has cost {}'.format(author_id, cost))
                    # self.stdout.write('{} / {} / {}'.format(cost, factor, inv_fee))
                    payout = (cost / factor * credits * inv_fee).quantize(Decimal('.01'), rounding=ROUND_DOWN)
                    assert payout >= 0

                    if payout > 0:
                        if not dry_run:
                            Transaction.objects.create(
                                from_newspaper_id=newspaper_id,
                                to_user_id=author_id,
                                credits=payout,
                                kind=Transaction.NEWSPAPER_SUBSCRIPTION
                            )
                        remainder -= payout

                        if verbosity > 0:
                            username = User.objects.get(id=author_id).username
                            self.stdout.write(' pay {} credits to author {}'.format(payout, username))

                        clear_credits_cache(user_id=author_id)

                if total < newspaper.price:
                    editor_cost = newspaper.price - total
                    payout = (editor_cost / factor * credits * inv_fee).quantize(Decimal('.01'), rounding=ROUND_DOWN)
                    assert payout >= 0

                    if payout > 0:
                        if not dry_run:
                            Transaction.objects.create(
                                from_newspaper_id=newspaper_id,
                                to_user_id=newspaper.editor_id,
                                credits=payout,
                                kind=Transaction.NEWSPAPER_SUBSCRIPTION
                            )
                        remainder -= payout

                        if verbosity > 0:
                            username = User.objects.get(id=newspaper.editor_id).username
                            self.stdout.write(' pay {} credits to editor {}'.format(payout, username))
                else:
                    if verbosity > 0:
                        self.stdout.write(' not enough credits to pay editor (issue cost is {}, but price is {})'.format(
                            total.quantize(Decimal('.01')), newspaper.price))

                if remainder > 0:
                    if verbosity > 0:
                        self.stdout.write(' pay {} credits to platform as fee'.format(remainder, username))

                    if not dry_run:
                        Transaction.objects.create(
                            from_newspaper_id=newspaper_id,
                            to_platform=True,
                            credits=remainder,
                            kind=Transaction.NEWSPAPER_SUBSCRIPTION
                        )

                clear_credits_cache(newspaper_id=newspaper_id, platform=True)

        counter_end = time.perf_counter()
        self.stdout.write("{:%Y-%m-%d %H:%M:%S %z}: pay editors finished in {} / {} credits transfered".format(
            timezone.now(), timedelta(seconds=counter_end - counter_start), counter_total))
