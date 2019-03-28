import rapidjson as json

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

from utils.json import JsonResponse


@require_POST
def add(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key'], payload['value']]
    if 'timeout' in payload:
        args.append(payload['timeout'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.add(*args)
    return JsonResponse({'value': res})


@require_POST
def get(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'default' in payload:
        args.append(payload['default'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.get(*args)
    return JsonResponse({'value': res})


@require_POST
def set(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key'], payload['value']]
    if 'timeout' in payload:
        args.append(payload['timeout'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.set(*args)
    return JsonResponse({'value': res})


@require_POST
def touch(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'timeout' in payload:
        args.append(payload['timeout'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.touch(*args)
    return JsonResponse({'value': res})


@require_POST
def delete(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.delete(*args)
    return JsonResponse({'value': res})


@require_POST
def get_many(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['keys']]
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.get_many(*args)
    return JsonResponse({'value': res})


@require_POST
def get_or_set(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key'], payload['value']]
    if 'timeout' in payload:
        args.append(payload['timeout'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.get_or_set(*args)
    return JsonResponse({'value': res})


@require_POST
def has_key(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.has_key(*args)  # NOQA
    return JsonResponse({'value': res})


@require_POST
def incr(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'delta' in payload:
        args.append(payload['delta'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.incr(*args)
    return JsonResponse({'value': res})


@require_POST
def decr(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['key']]
    if 'delta' in payload:
        args.append(payload['delta'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.decr(*args)
    return JsonResponse({'value': res})


@require_POST
def set_many(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['data']]
    if 'timeout' in payload:
        args.append(payload['timeout'])
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.set_many(*args)
    return JsonResponse({'value': res})


@require_POST
def delete_many(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    args = [payload['keys']]
    if 'version' in payload:
        args.append(payload['version'])
    res = cache.delete_many(*args)
    return JsonResponse({'value': res})


@require_POST
def clear(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload.get('apikey') != settings.REMOTE_CACHE_API_KEY:
        return HttpResponseForbidden
    res = cache.clear()
    return JsonResponse({'value': res})
