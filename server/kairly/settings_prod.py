from .settings import *  # NOQA

DEBUG = False

# I am curious why production site need this to get admin working
# Without trusted origin admin raises error
# Error: CSRF Failed: Referer checking failed - ... does not match any trusted origins.
CSRF_TRUSTED_ORIGINS = ['kairly.com']

# enable loggind errors to console on production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'store4.rosti.cz',
        'NAME': 'kairly_2_265101',
        'USER': 'kairly_2_265101',
        'PASSWORD': 'RV3by6&#qg8@',
        'CONN_MAX_AGE': 570,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

ALLOWED_HOSTS = [
    'kairly.com',
    'kairly-2648.rostiapp.cz'
]

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ['localhost:6379'],
        'TIMEOUT': 86400 * 14,
    }
}

# error logs are sent using smtp backend
EMAIL_HOST = 'smtp.rosti.cz'
EMAIL_HOST_USER = '2648@rostiapp.cz'
EMAIL_HOST_PASSWORD = '4c0e19fa5bae44c2bbf26b0a11ef11dd'

# other mails are sent by SendInBlue
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

# STATICFILES_DIRS = (
#     '/srv/kairly/kairly-client/dist/static',
# )
#
# TEMPLATES[0]['DIRS'] = (
#     '/srv/kairly/kairly-client/dist',
# )

MEDIA_ROOT = '/srv/kairly/server/media'

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

TWITTER_KEYS = [
    # farin_cz / Kairly https://developer.twitter.com/en/apps/15312678
    {
        'CONSUMER_KEY': 'vYuzgkErlgcU8hLSDG0yS8gry',
        'CONSUMER_SECRET': 'U0hVZVDahNoC4r9imOPkyKLQCJE343h2YK6OcD5s47RD2tSUYK',
        'ACCESS_TOKEN_KEY': '321647013-HGaOJzhg6hfrNYfWGj1NsV6ufNLgNb2fdUbeNi2j',
        'ACCESS_TOKEN_SECRET': 'CchNp5KVcuzatUNzVZOZMOMh716CNTDoSsTGBTJg7XOhZ',
    }
]
