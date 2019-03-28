import rapidjson as json

from django.http import HttpResponse


def datetime_isoformat_ecma262(d):
    # https://github.com/django/django/blob/master/django/core/serializers/json.py
    r = d.isoformat()
    if d.microsecond:
        r = r[:23] + r[26:]
    if r.endswith('+00:00'):
        r = r[:-6] + 'Z'
    return r


class JsonResponse(HttpResponse):
    """JsonResponse using rapidjson"""

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super().__init__(content=json.dumps(data), **kwargs)
