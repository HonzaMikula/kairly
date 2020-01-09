import rapidjson as json
from functools import wraps
from collections import defaultdict

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


_entity_keys = {}


def entities_key(key, priority):
    def decorator(cls):
        _entity_keys[cls] = (key, priority)
        return cls
    return decorator


class Entities:

    def __init__(self, user, tzinfo=None):
        self.entities = defaultdict(set)
        self.loaded = defaultdict(dict)

        self.user = user
        self.tzinfo = user.tzinfo if tzinfo is None else tzinfo

        # to json on items can also add new object, we need to track this updates
        # and put them to result too
        self.called_from_to_json = False
        self.to_json_entities = None

    def __str__(self):
        return str(self.entities)

    def add(self, cls, id_or_object):
        if isinstance(id_or_object, int):
            object_id = id_or_object
        else:
            object_id = id_or_object.id
            self.loaded[cls][object_id] = id_or_object

        if self.called_from_to_json:
            if cls not in self.entities or object_id not in self.entities[cls]:
                self.to_json_entities[cls].add(object_id)
        else:
            self.entities[cls].add(object_id)

    def add_json(self, cls, data):
        self.loaded[cls][data['id']] = data
        self.entities[cls].add(data['id'])

    def update(self, other):
        for cls, ids in other.entities.items():
            self.entities[cls].update(ids)
        for cls, objects in other.loaded.items():
            self.loaded[cls].update(objects)

    def to_json(self):
        data = defaultdict(dict)

        def key_fn(cls):
            try:
                return _entity_keys[cls][1]
            except KeyError:
                raise ValueError(f'Missing @entities_key for {cls.__name__}')

        def entities_to_json(entities):
            for cls in sorted(entities.keys(), key=key_fn):
                ids = entities[cls]
                objects = {}

                if ids:
                    to_load = ids - self.loaded[cls].keys()
                    for obj in cls.objects.filter(id__in=list(to_load)):
                        self.loaded[cls][obj.id] = obj

                    for obj in self.loaded[cls].values():
                        if isinstance(obj, dict):
                            objects[obj['id']] = obj
                        else:
                            objects[getattr(obj, 'public_id', str(obj.id))] = obj.to_json(self)

                data[cls].update(objects)

        self.called_from_to_json = True
        self.to_json_entities = defaultdict(set)

        entities_to_json(self.entities)
        while self.to_json_entities:
            entities_to_json(self.to_json_entities)
            self.to_json_entities = defaultdict(set)

        self.called_from_to_json = False
        self.to_json_entities = None

        # sort result, map keys
        result = {}
        for cls in sorted(data.keys(), key=key_fn):
            result['$' + _entity_keys[cls][0]] = data[cls]

        return result


def entities_json_response(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        request, *tail = args

        entities = Entities(user=request.user)
        resp = view(request, entities, *tail, **kwargs)

        if isinstance(resp, HttpResponse):
            assert not isinstance(resp, JsonResponse) or resp.status_code > 299, "Return plain date instead of JsonResponse. It will be updated with entities"
            return resp

        resp.update(entities.to_json())
        return JsonResponse(resp)
    return wrapper
