from .settings_dev import *  # NOQA

DEBUG = True

# in local, if error mailing is tested, don't send mails to prod email account
ADMINS = (
    ('Roman Krejcik', 'farin1@gmail.com'),
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'kairly',
        'USER': 'root',
        'PASSWORD': '',
        'CONN_MAX_AGE': None,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ['localhost:6379'],
        'TIMEOUT': 300,
        'OPTIONS': {
            'DB': 5,
        },
    }
}

THUMBNAIL_REDIS_DB = 6

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

TWITTER_KEYS = [
    # @farin_cz / Kairly https://developer.twitter.com/en/apps/15312678
    {
        'CONSUMER_KEY': 'vYuzgkErlgcU8hLSDG0yS8gry',
        'CONSUMER_SECRET': 'U0hVZVDahNoC4r9imOPkyKLQCJE343h2YK6OcD5s47RD2tSUYK',
        'ACCESS_TOKEN_KEY': '321647013-HGaOJzhg6hfrNYfWGj1NsV6ufNLgNb2fdUbeNi2j',
        'ACCESS_TOKEN_SECRET': 'CchNp5KVcuzatUNzVZOZMOMh716CNTDoSsTGBTJg7XOhZ',
    }
]

# EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

ENABLE_PERFORMANCE_TIMER = True
