from django.db.models import Q
from django.http import HttpResponseForbidden

from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from .models import Transaction
from .utils import get_user_credits, get_platform_credits, clear_credits_cache


@ajax_login_required
def get_transactions(request):
    transactions = list(Transaction.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
                        .order_by('-created'))

    return JsonResponse({
        "credits": str(get_user_credits(request.user.id)),
        "transactions": [t.to_json(reversed=bool(t.from_user_id)) for t in transactions]
    })


@ajax_login_required
def get_platform_transactions(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    transactions = list(Transaction.objects.filter(Q(from_platform=True) | Q(to_platform=True))
                        .order_by('-created'))

    return JsonResponse({
        "credits": str(get_platform_credits()),
        "transactions": [t.to_json(reversed=bool(t.from_platform)) for t in transactions]
    })


@ajax_login_required
def buy_credits(request):
    balance = get_user_credits(request.user.id)
    if balance >= 2500:
        return HttpResponseForbidden("Greedy!")

    amount = 200

    Transaction.objects.create(
        from_platform=True,
        to_user_id=request.user.id,
        kind=Transaction.FREE_CREDIT,
        credits=amount,
    )

    clear_credits_cache(user_id=request.user.id, platform=True)

    return JsonResponse({
        "credits": str(balance+amount),
    })
