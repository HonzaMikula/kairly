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
