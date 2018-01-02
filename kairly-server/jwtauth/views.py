import jwt
import json

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def get_token(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user:
        payload = {'user_id': user.id}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({
            'token': token.decode('ascii')
        })
    else:
        return HttpResponse('Unauthorized', status=401)
