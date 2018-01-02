from functools import wraps

from django.http import HttpResponse


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        print(request.user)
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        return view(request, *args, **kwargs)
    return wrapper
