import jwt

from django.conf import settings
from django.contrib.auth import get_user_model


def JwtAuthenticationMiddleware(get_response):
    def middleware(request):
        if 'Authorization' in request.META and request.user.is_anonymous:
            token = request.META['Authorization'].replace('Bearer ', '')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = get_user_model().objects.get(username=payload['username'])
        return get_response(request)

    return middleware
