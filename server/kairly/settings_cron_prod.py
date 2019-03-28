from .settings_prod import *  # NOQA

CACHES = {
    'default': {
        'BACKEND': 'remotecache.backends.RemoteCache',
        'LOCATION': 'https://kairly-2648.rostiapp.cz/cache',
    }
}
