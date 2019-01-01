from django.core.management.base import BaseCommand
from django.db import transaction

from credits.models import Transaction
from credits.utils import clear_credits_cache
from users.models import User


class Command(BaseCommand):
    help = 'Add free credits to all active users'

    DEFAULT_AMOUNT = 350

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            action='store',
            dest='amount',
            help=f'Amount of credits (default {self.DEFAULT_AMOUNT})',
        )
        parser.add_argument(
            '--user',
            action='store',
            dest='user',
            help='Add to single user only',
        )

    def handle(self, *args, **options):
        user = options.get('user')
        amount = int(options.get('amount') or self.DEFAULT_AMOUNT)

        with transaction.atomic():
            if user:
                user_ids = [User.objects.get(username=user).id]
            else:
                user_ids = User.objects.filter(is_active=True).values_list('id', flat=True)
            transactions = [
                Transaction(
                    from_platform=True,
                    to_user_id=id,
                    kind=Transaction.FREE_CREDIT,
                    credits=amount,
                )
                for id in user_ids
            ]
            Transaction.objects.bulk_create(transactions)

            for t in transactions:
                clear_credits_cache(user_id=t.to_user.id)
