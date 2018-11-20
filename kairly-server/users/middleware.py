import logging

import jwt
from jwt.exceptions import PyJWTError


from pytz import timezone, UnknownTimeZoneError

from django.conf import settings
from django.contrib.auth import get_user_model


def JwtAuthenticationMiddleware(get_response):
    def middleware(request):
        if 'HTTP_AUTHORIZATION' in request.META and request.user.is_anonymous:
            bearer, token = request.META['HTTP_AUTHORIZATION'].split(' ', maxsplit=1)
            User = get_user_model()
            try:
                # TEMPORARY HACK, ACCEPT EXPIRED TOKENS
                # BACAUSE OLD CLIENT MAKES INFINITE REDIRECT FOR SUCH TOKENS
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], verify=False)
                request.user = User.objects.get(id=payload.get('uid'))
            except (User.DoesNotExist, PyJWTError) as e:
                logging.error(str(e))
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
