import rapidjson as json
from django.db import transaction
from django.views.decorators.http import require_POST

from utils.decorators import ajax_login_required
from utils.json import JsonResponse


@ajax_login_required
@require_POST
@transaction.atomic
def import_rss(request):
    payload = json.loads(request.body.decode('utf-8'))
    print(payload['sources'])

    return JsonResponse({})
