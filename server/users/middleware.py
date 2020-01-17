import logging

import jwt
from jwt.exceptions import PyJWTError


from pytz import timezone, UnknownTimeZoneError

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


def JwtAuthenticationMiddleware(get_response):
    def middleware(request):
        user = None
        if 'HTTP_AUTHORIZATION' in request.META:
            try:
                bearer, token = request.META['HTTP_AUTHORIZATION'].split(' ', maxsplit=1)
                User = get_user_model()
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except PyJWTError as e:
                logging.error(str(e))
                payload = None
            except ValueError:
                # wrong header, can't split
                payload = None

            if payload:
                try:
                    user = User.objects.get(id=payload.get('uid'))
                except User.DoesNotExist as e:
                    logging.error(str(e))

        if (request.is_ajax() and not request.path.startswith('/api/autocomplete/')) or user:
            if user:
                request.user = user
            else:
                if not request.user.is_anonymous:
                    request.user = AnonymousUser()

        # from utils.debug import perf_timer
        # with perf_timer(f"{request.path} get response"):
        return get_response(request)

    return middleware


def AnonymousUserTimeZoneMiddleware(get_response):
    def middleware(request):
        if request.user.is_anonymous:
            name = request.META.get('HTTP_X_TIMEZONE', '')
            try:
                tzinfo = timezone(name)
            except UnknownTimeZoneError:
                tzinfo = timezone('Europe/Prague')
            request.user.tzinfo = tzinfo
        return get_response(request)
    return middleware
