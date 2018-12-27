from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.core.cache import cache
from .models import Transaction


AUTHOR_CREDITS_CACHE_KEY = 'balance:author:{}'
NEWSPAPER_CREDITS_CACHE_KEY = 'balance:newspaper:{}'
USER_CREDITS_CACHE_KEY = 'balance:user:{}'


def get_author_retained_credits(user):
    cache_key = AUTHOR_CREDITS_CACHE_KEY.format(user.id)
    balance = cache.get(cache_key)
    if balance is None:
        expenses = Transaction.objects.filter(from_author=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_author=user).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def get_newspaper_retained_credits(newspaper):
    cache_key = NEWSPAPER_CREDITS_CACHE_KEY.format(newspaper.id)
    balance = cache.get(cache_key)
    if balance is None:
        expenses = Transaction.objects.filter(from_newspaper=newspaper).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_newspapers=newspaper).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


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


def clear_credits_cache(*, author=None, user=None, newspaper=None):
    def clear_cache():
        keys = []
        if author is not None:
            keys.append(AUTHOR_CREDITS_CACHE_KEY.format(author.id))
        if newspaper is not None:
            keys.append(NEWSPAPER_CREDITS_CACHE_KEY.format(newspaper.id))
        if user is not None:
            keys.append(USER_CREDITS_CACHE_KEY.format(user.id))
        cache.delete_many(keys)
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
    clear_credits_cache(user=user, author=subscription.author)


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
    clear_credits_cache(user=user, newspaper=subscription.newspaper)
