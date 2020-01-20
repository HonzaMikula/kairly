import orjson as json
from functools import wraps
from collections import defaultdict

from django.db import models
from django.core.cache import cache
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
    """JsonResponse using orjson"""

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super().__init__(content=json.dumps(data), **kwargs)


_entity_keys = {}


def entities_key(key, priority):
    def decorator(cls):
        _entity_keys[cls] = (key, priority)
        return cls
    return decorator


def json_key_for_class(cls):
    return '$' + _entity_keys[cls][0]


class Ref:

    def __init__(self, cls, id):
        self.cls = cls
        self.id = id

    def __eq__(self, other):
        return self.cls == other.cls and self.id == other.id

    def __hash__(self):
        return hash((self.cls, self.id))

    def __repr__(self):
        return f"ref<{self.cls.__name__}:{self.id}"

    @property
    def cache_key(self):
        return f"ref-{self.cls._meta}-{self.id}"


class MappedRef:

    def __init__(self, ref, template):
        self.ref = ref
        self.template = template


class Entity:

    def __init__(self, ref, instance=None):
        self.ref = ref
        self.instance = instance
        self.json_id = None
        self.json_data = None
        self.deps = None


class Entities:

    def __init__(self, user, tzinfo=None):
        self.entities = defaultdict(dict)  # to change to plain dict
        self.unfulfilled_entities = defaultdict(list)

        self.user = user
        self.tzinfo = user.tzinfo if tzinfo is None else tzinfo

        self.track_references = None  # set with all touched refs

    def __str__(self):
        tokens = []
        for cls, entities in self.entities.items():
            tokens.append(cls.__name__)
            tokens.append('\n ')
            tokens.extend(f" {id}:{ent.json_id if ent.json_id else '___'}:{'X' if ent.json_data else '_'}" for id, ent in entities.items())
            tokens.append('\n')
        return ''.join(tokens)

    @property
    def fulfilled(self):
        for entities in self.unfulfilled_entities.values():
            if entities:
                return False
        return True

    def make_ref(self, cls, id_or_instance):
        if isinstance(id_or_instance, int):
            object_id = id_or_instance
            instance = None
        elif isinstance(id_or_instance, models.Model):
            object_id = id_or_instance.id
            instance = id_or_instance
        else:
            raise TypeError("Wrong object type")
        assert isinstance(object_id, (int, str))

        ent = self.entities[cls].get(object_id)
        if ent is None:
            ref = Ref(cls, object_id)
            ent = Entity(ref, instance)
            self.entities[cls][object_id] = ent
            self.unfulfilled_entities[cls].append(ent)
        else:
            ref = ent.ref
            if ent.instance is None and instance is not None:
                ent.instance = instance

        if self.track_references is not None:
            self.track_references.add(ref)
        return ref

    def add_references(self, refs):
        for ref in refs:
            self.make_ref(ref.cls, ref.id)

    def _fill(self, ent, data):
        # HACK for now, this method shouldn't know about full name
        json_id = data.get('id') or data['fullName']
        fragment = {}
        fragment[json_id] = data
        ent.json_id = json_id
        ent.json_data = fragment

    def to_json_fragment(self):
        def key_fn(cls):
            try:
                return _entity_keys[cls][1]
            except KeyError:
                raise ValueError(f'Missing @entities_key for {cls.__name__}')

        def get_cache_value(ent):
            return (ent.json_id, ent.json_data, [(dep.cls, dep.id) for dep in ent.deps])

        def fill(ent):
            ent.deps = self.track_references = set()
            data = ent.instance.to_json(self)
            self._fill(ent, data)
            self.track_references = None

        cache_write = []

        # entity to json may add new references, go through loop until no new was added
        while not self.fulfilled:
            classes = list(sorted(self.unfulfilled_entities.keys(), key=key_fn))
            for cls in classes:
                ents = self.unfulfilled_entities[cls]
                del self.unfulfilled_entities[cls]

                cached = cache.get_many([ent.ref.cache_key for ent in ents])

                to_load = []
                for ent in ents:
                    cached_ent = cached.get(ent.ref.cache_key)
                    if cached_ent:
                        json_id, json_data, deps = cached_ent
                        ent.json_id = json_id
                        ent.json_data = json_data
                        ent.deps = [self.make_ref(dep_cls, dep_id) for dep_cls, dep_id in deps]
                    else:
                        if ent.instance is None:
                            to_load.append(ent.ref.id)
                        else:
                            cache_write.append(ent)
                            fill(ent)

                if to_load:
                    for instance in cls.objects.filter(id__in=to_load):
                        ent = self.entities[cls][instance.id]
                        ent.instance = instance
                        cache_write.append(ent)
                        fill(ent)

        result = []
        for i, cls in enumerate(sorted(self.entities.keys(), key=key_fn)):
            result.append(b',"' if i else b'"')
            result.append(json_key_for_class(cls).encode())
            result.append(b'":{')
            for j, ref in enumerate(self.entities[cls].values()):
                if j:
                    result.append(b',')
                if not isinstance(ref.json_data, bytes):
                    ref.json_data = json.dumps(ref.json_data, default=self.json_dumps_default)[1:-1]
                result.append(ref.json_data)
            result.append(b'}')

        # cache after json_data was converted to bytes
        if cache_write:
            data = {ent.ref.cache_key: get_cache_value(ent) for ent in cache_write}
            cache.set_many(data, timeout=None)

        if result:
            return b''.join(result)
        return None

    def json_dumps_default(self, obj):
        def get_entity(ref):
            ent = self.entities[ref.cls][ref.id]
            if ent.json_id is None:
                # exception is replace by generic one in orjson, so print source id there
                # should never happen, this is more like assert
                print(f"Entity is not fulfilled {ref}")
                raise AssertionError
            return ent

        if isinstance(obj, Ref):
            return get_entity(obj).json_id
        if isinstance(obj, MappedRef):
            return obj.template.format(get_entity(obj.ref).json_id)
        raise TypeError


def entities_json_response(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        request, *tail = args

        from utils.debug import perf_timer
        with perf_timer('{} entities_json_response', request.path) as timer:
            entities = Entities(user=request.user)
            resp = view(request, entities, *tail, **kwargs)

            timer('{} render view response', request.path)

            if isinstance(resp, HttpResponse):
                assert not isinstance(resp, JsonResponse) or resp.status_code > 299, "Return plain date instead of JsonResponse. It will be updated with entities"
                return resp

            # entities must be dumped before response itself is dumped
            # because referencese need to be filled with json ids
            fragment = entities.to_json_fragment()
            timer('{} dump entities JSON fragment', request.path)

            resp = json.dumps(resp, default=entities.json_dumps_default)
            timer('{} dump resp JSON', request.path)

            if fragment is not None:
                resp = resp[:-1] + b',' + fragment + b'}'

            timer('{} update response with entities', request.path)
            return HttpResponse(resp, content_type='application/json')

    return wrapper
