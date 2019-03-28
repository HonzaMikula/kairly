import requests

from django.conf import settings
from django.core.cache.backends.base import BaseCache

UNDEF = object()


class RemoteCache(BaseCache):

    def __init__(self, base_url, params):
        super().__init__(params)
        self.base_url = base_url.rstrip('/')

    def add(self, key, value, timeout=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
            'value': value,
        }
        if timeout is not UNDEF:
            payload['timeout'] = timeout
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/add', json=payload)
        return resp.json()['value']

    def get(self, key, default=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if default is not UNDEF:
            payload['default'] = default
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/get', json=payload)
        return resp.json()['value']

    def set(self, key, value, timeout=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
            'value': value,
        }
        if timeout is not UNDEF:
            payload['timeout'] = timeout
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/set', json=payload)
        return resp.json()['value']

    def touch(self, key, timeout=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if timeout is not UNDEF:
            payload['timeout'] = timeout
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/touch', json=payload)
        return resp.json()['value']

    def delete(self, key, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/delete', json=payload)
        return resp.json()['value']

    def get_many(self, keys, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'keys': keys,
        }
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/get_many', json=payload)
        return resp.json()['value']

    def get_or_set(self, key, default, timeout=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
            'default': default,
            'timeout': timeout,
        }
        if timeout is not UNDEF:
            payload['timeout'] = timeout
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/get_or_set', json=payload)
        return resp.json()['value']

    def has_key(self, key, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/has_key', json=payload)
        return resp.json()['value']

    def incr(self, key, delta=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if delta is not UNDEF:
            payload['delta'] = delta
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/incr', json=payload)
        return resp.json()['value']

    def decr(self, key, delta=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'key': key,
        }
        if delta is not UNDEF:
            payload['delta'] = delta
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/decr', json=payload)
        return resp.json()['value']

    def set_many(self, data, timeout=UNDEF, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'data': data,
        }
        if timeout is not UNDEF:
            payload['timeout'] = timeout
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/set_many', json=payload)
        return resp.json()['value']

    def delete_many(self, keys, version=UNDEF):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY,
            'keys': keys,
        }
        if version is not UNDEF:
            payload['version'] = version
        resp = requests.post(f'{self.base_url}/delete_many', json=payload)
        return resp.json()['value']

    def clear(self):
        payload = {
            'apikey': settings.REMOTE_CACHE_API_KEY
        }
        resp = requests.post(f'{self.base_url}/clear', json=payload)
        return resp.json()['value']
