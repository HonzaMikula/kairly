from datetime import timedelta, timezone
import jwt
from jwt.exceptions import DecodeError

from django.conf import settings
from django.contrib.auth import get_user_model


def JwtAuthenticationMiddleware(get_response):
    def middleware(request):
        if 'HTTP_AUTHORIZATION' in request.META and request.user.is_anonymous:
            bearer, token = request.META['HTTP_AUTHORIZATION'].split(' ', maxsplit=1)
            User = get_user_model()
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user = User.objects.get(id=payload.get('uid'))
            except (User.DoesNotExist, DecodeError) as e:
                print(e)
                pass
        return get_response(request)

    return middleware


def UserTimeZoneMiddleware(get_response):
    def middleware(request):
        timezone_offset = int(request.META.get('HTTP_X_TIMEZONE', 0))
        request.tzinfo = timezone(timedelta(minutes=-timezone_offset))
        return get_response(request)

    return middleware
