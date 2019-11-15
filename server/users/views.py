import logging
import time
import urllib.error
import urllib.request
from decimal import Decimal

import jwt
import rapidjson as json
from dal import autocomplete
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils.timezone import localdate
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from libgravatar import Gravatar
from pytz import UnknownTimeZoneError, timezone

from articles.models import Newspaper
from credits.utils import get_user_credits
from utils.db import get_column_if_duplicate
from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from utils.upload import file_from_data_uri
from .models import User, ExploreTimeline

TOKEN_EXPIRATION = 30 * 86400

logger = logging.getLogger(__name__)


def issue_token(user):
    now = int(time.time())
    payload = {
        'uid': user.id,
        'iat': now,
        'exp': now + TOKEN_EXPIRATION,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@require_POST
@csrf_exempt
def get_token(request):
    data = json.loads(request.body.decode())
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user:
        return JsonResponse({
            'token': issue_token(user)
        })
    else:
        return HttpResponse('Unauthorized', status=401)


@ajax_login_required
def refresh_token(request):
    return JsonResponse({
        'token': issue_token(request.user)
    })


class ProfileView(View):
    @ajax_login_required
    def get(self, request):
        newspapers = []
        for newspaper in Newspaper.objects.filter(Q(editor=request.user) | Q(co_editors=request.user)).values_list('id', 'editor__username', 'slug', 'title', named=True):
            full_name = '{}/{}'.format(newspaper.editor__username, newspaper.slug)
            newspapers.append({
                'fullName': full_name,
                'title': newspaper.title,
            })

        today = localdate()
        start = request.user.activity_history_start
        history = request.user.activity_history
        if start != today or history & 1 == 0:
            shift = (today - start).days
            history = (history << shift) | 1
            history &= (1 << 63) - 1  # pad to 62 days
            request.user.activity_history_start = today
            request.user.activity_history = history
            request.user.save()

        user = request.user.to_json(owner=True)
        user['newspapers'] = newspapers
        user['credits'] = str(get_user_credits(request.user.id))

        return JsonResponse({
            "user": user
        })

    @ajax_login_required
    def patch(self, request):
        payload = json.loads(request.body.decode('utf-8'))
        user = request.user
        fields = ['name', 'bio', 'medium', 'timezone']
        for field in fields:
            if field in payload:
                setattr(user, field, payload[field])

        if 'price' in payload:
            price = Decimal(payload['price'])
            if price not in settings.ALLOWED_PRICE_LEVELS:
                return JsonResponse({'error': 'invalid price'}, status=400)
            user.price = price

        integrations = payload.get('integrations', {})
        if 'twitter' in integrations:
            value = integrations['twitter']
            user.twitter_account = value if value else None

        if 'picture' in payload:
            picture = file_from_data_uri(payload['picture'], user.username)
            user.picture = picture

        user.save()
        return JsonResponse(user.to_json(owner=True))


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

    name = request.META.get('HTTP_X_TIMEZONE', '')
    try:
        tzinfo = timezone(name)
    except UnknownTimeZoneError:
        tzinfo = timezone('GMT')

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            picture=picture,
            medium='',
            bio='',
            timezone=str(tzinfo)
        )
    except IntegrityError as e:
        name = get_column_if_duplicate(e)
        if name == 'username':
            return JsonResponse({'error': 'Username is already taken.'}, status=400)
        raise
    return JsonResponse(user.to_json())


@require_POST
def change_password(request):
    payload = json.loads(request.body.decode('utf-8'))
    user = request.user
    token = payload.get('token')

    if token:
        signer = TimestampSigner(salt='v1')
        try:
            username = signer.unsign(token, max_age=settings.RESET_PASSWORD_TOKEN_MAX_AGE)
            user = User.objects.get(username=username)
        except SignatureExpired:
            return JsonResponse({'error': 'Token is expired'}, status=400)
        except (BadSignature, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=400)

        if not cache.get(f'reset_password:{token}'):
            return JsonResponse({'error': 'Token is used or expired'}, status=400)

    if user.is_anonymous:
        return HttpResponse(status=401)

    if not token and not user.check_password(payload['oldPassword']):
        return JsonResponse({'error': 'Wrong old password.'}, status=400)

    password = payload['newPassword']
    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({'error': ' '.join(e.messages)}, status=400)

    user.set_password(password)
    user.save()

    if token and not settings.RESET_PASSWORD_TOKEN_ALLOW_REUSE:
        cache.delete(f'reset_password:{token}')

    return JsonResponse(user.to_json())


@require_POST
def reset_password(request):
    payload = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(email=payload.get('email'))
    except User.DoesNotExist:
        # fail silently
        return JsonResponse({})

    token = TimestampSigner(salt='v1').sign(user.username)
    logging.info(f"Password reset token generated for {user.username}: {token}")

    # use additional security level, even with compromised SECRET_KEY
    # attacker can't simply reset password just by generating any valid token
    # out of backend
    cache.set(f'reset_password:{token}', 1, settings.RESET_PASSWORD_TOKEN_MAX_AGE)

    message = EmailMessage(
        subject=None,  # required for SendinBlue templates
        body=None,  # required for SendinBlue templates
        to=[user.email]
    )

    message.from_email = None  # required for SendinBlue templates
    message.template_id = 1  # use this SendinBlue template
    message.merge_global_data = {
        'RESET_URL': f"https://kairly.com/reset-password/{token}",
    }
    message.send()
    return JsonResponse({})


def explore_tab(request, tab):
    explore = get_object_or_404(ExploreTimeline, slug=tab)
    ids = set()
    for cat in explore.content['authors']:
        for author_id in cat['authors']:
            ids.add(author_id)

    users = {}
    for user in User.objects.filter(username__in=list(ids)):
        users[user.username] = user

    categories = []
    for cat in explore.content['authors']:
        categories.append({
            'name': cat['en'],
            'authors': [users[username].to_json() for username in cat['authors']],
        })

    return JsonResponse({
        'newspapers': explore.content['newspapers'],
        'categories': categories
    })


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(username__istartswith=self.q)

        return qs


# def query_user(request):
#     query = request.GET['q']
#     users = User.objects\
#         .filter(kind=User.PERSONAL, is_active=True)\
#         .filter(username__istartswith=query)

#     return JsonResponse({
#         'items': [user.to_json() for user in users[:20]]
#     })
