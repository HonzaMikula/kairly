from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.core.cache import cache
from .models import Transaction


USER_CREDITS_CACHE_KEY = 'balance_{}'


def get_user_credits(user):
    cache_key = USER_CREDITS_CACHE_KEY.format(user.id)
    balance = cache.get(cache_key)
    if balance is None:
        expenses = Transaction.objects.filter(from_user=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_user=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def on_credits_change(user):
    def clear_cache():
        cache.delete(USER_CREDITS_CACHE_KEY.format(user.id))
    transaction.on_commit(clear_cache)


def pay_author_subscription(subscription):
    user = subscription.user
    price = subscription.author.price
    if price > 0:
        Transaction.objects.create(
            from_user=user,
            to_author=subscription.author,
            credits=price,
            kind=Transaction.AUTHOR_SUBSCRIPTION
        )
    if subscription.donation > 0:
        Transaction.objects.create(
            from_user=user,
            to_author=subscription.author,
            credits=subscription.donation,
            kind=Transaction.DONATION
        )
    on_credits_change(user)


def pay_newspaper_subscription(subscription):
    user = subscription.user
    price = subscription.newspaper.price
    if price > 0:
        Transaction.objects.create(
            from_user=user,
            to_newspaper=subscription.newspaper,
            credits=price,
            kind=Transaction.NEWSPAPER_SUBSCRIPTION
        )
    if subscription.donation > 0:
        Transaction.objects.create(
            from_user=user,
            to_newspaper=subscription.newspaper,
            credits=subscription.donation,
            kind=Transaction.DONATION
        )
    on_credits_change(user)
