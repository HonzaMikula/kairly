from .settings import *  # NOQA

# Unused for now, just use node dev server on :8080 for frontend endpoitns

MEDIA_SITE = 'http://localhost:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

RESET_PASSWORD_TOKEN_ALLOW_REUSE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}
