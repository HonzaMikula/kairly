from functools import wraps

from django.http import HttpResponse, HttpRequest


def ajax_login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        # common view -> request is first args
        # class based view -> request is second arg
        request = next(a for a in args if isinstance(a, HttpRequest))
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        return view(*args, **kwargs)
    return wrapper
