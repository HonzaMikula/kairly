from django.core.management.base import BaseCommand
from django.db import transaction

from credits.models import Transaction
from credits.utils import clear_credits_cache
from users.models import User


class Command(BaseCommand):
    help = 'Add free credits to all active users'

    DEFAULT_AMOUNT = 350

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='*', type=str, help='Users to assign credit')

        parser.add_argument(
            '--amount',
            action='store',
            dest='amount',
            help=f'Amount of credits (default {self.DEFAULT_AMOUNT})',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='Add to all users',
        )

    def handle(self, *args, **options):
        all = options.get('all')
        amount = int(options.get('amount') or self.DEFAULT_AMOUNT)

        with transaction.atomic():
            if all:
                user_ids = User.objects.filter(is_active=True).values_list('id', flat=True)
            else:
                usernames = options.get('usernames')
                if not usernames:
                    raise ValueError("No user given")
                user_ids = User.objects.filter(username__in=usernames).values_list('id', flat=True)
                if len(user_ids) != len(usernames):
                    raise ValueError("User does not exist.")

            verbosity = options.get('verbosity')
            if verbosity > 0:
                self.stdout.write("Assigning free cretids to {} users.".format(len(user_ids)))

            if amount == 0:
                raise ValueError("Amount can't be 0")

            if amount > 0:
                transactions = [
                    Transaction(
                        from_platform=True,
                        to_user_id=id,
                        kind=Transaction.FREE_CREDIT,
                        credits=amount,
                    )
                    for id in user_ids
                ]
            else:
                transactions = [
                    Transaction(
                        from_user_id=id,
                        to_platform=True,
                        kind=Transaction.FREE_CREDIT,
                        credits=-amount,
                    )
                    for id in user_ids
                ]
            Transaction.objects.bulk_create(transactions)

            for t in transactions:
                clear_credits_cache(user_id=t.to_user.id if t.to_user else t.from_user.id)
