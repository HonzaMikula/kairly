from django.db.models import Q

from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from .models import Transaction
from .utils import get_user_credits


@ajax_login_required
def get_transactions(request):
    transactions = list(Transaction.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
                        .order_by('-created'))

    return JsonResponse({
        "credits": str(get_user_credits(request.user.id)),
        "transactions": [t.to_json() for t in transactions]
    })
