import jwt
import json
import time
from collections import defaultdict
import urllib.request
import urllib.error

from libgravatar import Gravatar

from django.db.utils import IntegrityError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from utils.db import get_column_if_duplicate
from utils.decorators import ajax_login_required
from utils.upload import file_from_data_uri
from articles.models import Edition, EditionBacklog
from .models import User


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


class ProfileView(View):
    @ajax_login_required
    def get(self, request):
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
            "user": request.user.to_json(),
            "editions": editions,
            "backlog": backlog
        })

    @ajax_login_required
    def patch(self, request):
        payload = json.loads(request.body.decode('utf-8'))
        user = request.user
        fields = ['name', 'bio', 'medium', 'timezone']
        for field in fields:
            if field in payload:
                setattr(user, field, payload[field])

        if 'picture' in payload:
            picture = file_from_data_uri(payload['picture'], user.username)
            user.picture = picture

        user.save()
        return JsonResponse(user.to_json())


# TODO enable CSRF protection
@require_POST
def signup(request):
    payload = json.loads(request.body.decode('utf-8'))

    username = payload['username']
    email = payload['email']
    password = payload['password']

    try:
        User.username_validator(username)
        EmailValidator()(email)
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({'error': ' '.join(e.messages)}, status=400)

    g = Gravatar(email)
    picture = g.get_image(use_ssl=True, default='404')
    try:
        urllib.request.urlopen(picture)
    except urllib.error.HTTPError:
        picture = ''

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            picture=picture,
            medium='',
            bio='',
            timezone=str(request.tzinfo)
        )
    except IntegrityError as e:
        name = get_column_if_duplicate(e)
        if name == 'username':
            return JsonResponse({'error': 'Username is already taken.'}, status=400)
        raise
    return JsonResponse(user.to_json())


@require_POST
@ajax_login_required
def change_password(request):
    payload = json.loads(request.body.decode('utf-8'))
    user = request.user

    if not user.check_password(payload['oldPassword']):
        return HttpResponse('Unauthorized', status=401)

    password = payload['newPassword']
    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({'error': ' '.join(e.messages)}, status=400)

    user.set_password(password)
    user.save()
    return JsonResponse(user.to_json())
