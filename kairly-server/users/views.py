import jwt
import json
import time
from collections import defaultdict

from libgravatar import Gravatar

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from utils.decorators import ajax_login_required
from articles.models import Edition, EditionBacklog
from articles.serializers import author_json


@require_POST
@csrf_exempt
def get_token(request):
    data = json.loads(request.body.decode())
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user:
        payload = {
            'uid': user.id,
            'iat': int(time.time()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({
            'token': token.decode()
        })
    else:
        return HttpResponse('Unauthorized', status=401)


@ajax_login_required
def profile(request):
    g = Gravatar(request.user.email)

    # TODO load edition and backlog in separate endpoint
    editions = []
    internal_ids_mapping = {}
    for edition in Edition.objects.filter(editor=request.user).values_list('id', 'editor_id', 'slug', 'title', named=True):
        public_id = '{}/{}'.format(request.user.username, edition.slug)
        internal_ids_mapping[edition.id] = public_id
        editions.append({
            'id': public_id,
            'title': edition.title,
        })

    backlog = defaultdict(list)
    for bl in EditionBacklog.objects.filter(edition_id__in=internal_ids_mapping.keys()):
        backlog[bl.post_id].append(internal_ids_mapping[bl.edition_id])

    # TODO merge author and user props
    return JsonResponse({
        "user": {
            "name": request.user.get_full_name(),
            'picture': g.get_image(use_ssl=True, default='blank'),
            "author": author_json(request.user),
        },
        "editions": editions,
        "backlog": backlog
    })
