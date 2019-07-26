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
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.db.models import Count, Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils.timezone import localdate
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from libgravatar import Gravatar
from pytz import UnknownTimeZoneError, timezone

from articles.models import Newspaper
from credits.utils import get_user_credits
from utils.db import get_column_if_duplicate
from utils.decorators import ajax_login_required
from utils.json import JsonResponse
from utils.upload import file_from_data_uri
from .models import Category, CategoryUser, User

TOKEN_EXPIRATION = 30 * 86400


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
@ajax_login_required
def change_password(request):
    payload = json.loads(request.body.decode('utf-8'))
    user = request.user

    if not user.check_password(payload['oldPassword']):
        return JsonResponse({'error': 'Wrong old password.'}, status=400)

    password = payload['newPassword']
    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({'error': ' '.join(e.messages)}, status=400)

    user.set_password(password)
    user.save()
    return JsonResponse(user.to_json())


def reset_password(request):
    message = EmailMessage(
        subject=None,  # required for SendinBlue templates
        body=None,  # required for SendinBlue templates
        to=["farin@farin.cz"]  # single recipient...
        # ...multiple to emails would all get the same message
        # (and would all see each other's emails in the "to" header)
    )

    message.from_email = None  # required for SendinBlue templates
    message.template_id = 1  # use this SendinBlue template
    message.merge_global_data = {
        'RESET_URL': "https://kairly.com/reset?key=foo",
    }
    message.send()
    return JsonResponse({})


def explore_tab(request, tab):
    categories = []
    for category in Category.objects.filter(explore_tab=tab):
        cat_authors = CategoryUser.objects.filter(category=category).select_related('user').order_by('ordering', 'user__name')
        categories.append({
            'name': category.name,
            'authors': [cu.user.to_json() for cu in cat_authors],
        })

    if tab == 'Best of Kairly':
        categories.append({
            'name': 'New Authors',
            'authors': [
                u.to_json() for u in
                User.objects.exclude(kind=User.FEED)
                    .annotate(post_count=Count('post'))
                    .filter(post_count__gt=1)
                    .order_by('-date_joined')[:14]  # fill list + modal, each 7 items
            ]
        })

    return JsonResponse({
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
