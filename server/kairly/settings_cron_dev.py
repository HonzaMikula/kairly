from .settings_farin import *  # NOQA

CACHES = {
    'default': {
        'BACKEND': 'remotecache.backends.RemoteCache',
        'LOCATION': 'http://localhost:8000/cache',
    }
}
