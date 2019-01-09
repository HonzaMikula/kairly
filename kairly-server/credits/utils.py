from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.core.cache import cache
from .models import Transaction


AUTHOR_CREDITS_CACHE_KEY = 'balance:author:{}'
NEWSPAPER_CREDITS_CACHE_KEY = 'balance:newspaper:{}'
PLATFORM_CREDITS_CACHE_KEY = 'balance:platform'
USER_CREDITS_CACHE_KEY = 'balance:user:{}'


def get_author_retained_credits(id, snapshot=None):
    if snapshot:
        args = dict(created__lt=snapshot)
        cache_key = None
        balance = None
    else:
        args = {}
        cache_key = AUTHOR_CREDITS_CACHE_KEY.format(id)
        balance = cache.get(cache_key)

    if balance is None:
        expenses = Transaction.objects.filter(from_author_id=id, **args).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_author_id=id, **args).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        if cache_key:
            cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def get_newspaper_retained_credits(id, snapshot=None):
    if snapshot:
        args = dict(created__lt=snapshot)
        cache_key = None
        balance = None
    else:
        args = {}
        cache_key = NEWSPAPER_CREDITS_CACHE_KEY.format(id)
        balance = cache.get(cache_key)

    if balance is None:
        expenses = Transaction.objects.filter(from_newspaper_id=id, **args).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_newspaper_id=id, **args).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        if cache_key:
            cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def get_platform_credits():
    cache_key = PLATFORM_CREDITS_CACHE_KEY
    balance = cache.get(cache_key)
    if balance is None:
        expenses = Transaction.objects.filter(from_platform=True).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_platform=True).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def get_user_credits(id):
    cache_key = USER_CREDITS_CACHE_KEY.format(id)
    balance = cache.get(cache_key)
    if balance is None:
        expenses = Transaction.objects.filter(from_user_id=id).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        income = Transaction.objects.filter(to_user_id=id).aggregate(Sum('credits'))['credits__sum'] or Decimal(0)
        balance = income - expenses
        cache.set(cache_key, str(balance))
    else:
        balance = Decimal(balance)
    return balance


def clear_credits_cache(*, author_id=None, user_id=None, newspaper_id=None, platform=None):
    def clear_cache():
        keys = []
        if author_id is not None:
            keys.append(AUTHOR_CREDITS_CACHE_KEY.format(author_id))
        if newspaper_id is not None:
            keys.append(NEWSPAPER_CREDITS_CACHE_KEY.format(newspaper_id))
        if user_id is not None:
            keys.append(USER_CREDITS_CACHE_KEY.format(user_id))
        if platform:
            keys.append(PLATFORM_CREDITS_CACHE_KEY)
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
    clear_credits_cache(user_id=user.id, author_id=subscription.author_id)


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
    clear_credits_cache(user_id=user.id, newspaper_id=subscription.newspaper_id)
