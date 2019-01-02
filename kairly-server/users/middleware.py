import logging

import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError


from pytz import timezone, UnknownTimeZoneError

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


def JwtAuthenticationMiddleware(get_response):
    def middleware(request):
        user = None
        if 'HTTP_AUTHORIZATION' in request.META:
            bearer, token = request.META['HTTP_AUTHORIZATION'].split(' ', maxsplit=1)
            User = get_user_model()
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except ExpiredSignatureError:
                # TEMPORARY HACK, ACCEPT EXPIRED TOKENS
                # BACAUSE OLD CLIENT MAKES INFINITE REDIRECT FOR SUCH TOKENS
                logging.error("HACK: Expired token accepted")
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], verify=False)
            except PyJWTError as e:
                logging.error(str(e))
                payload = None

            if payload:
                try:
                    user = User.objects.get(id=payload.get('uid'))
                except User.DoesNotExist as e:
                    logging.error(str(e))

        if request.is_ajax() or user:
            if user:
                request.user = user
            else:
                if not request.user.is_anonymous:
                    request.user = AnonymousUser()

        return get_response(request)

    return middleware


def AnonymousUserTimeZoneMiddleware(get_response):
    def middleware(request):
        if request.user.is_anonymous:
            name = request.META.get('HTTP_X_TIMEZONE', '')
            try:
                tzinfo = timezone(name)
            except UnknownTimeZoneError:
                tzinfo = timezone('GMT')
            request.user.tzinfo = tzinfo
        return get_response(request)
    return middleware
