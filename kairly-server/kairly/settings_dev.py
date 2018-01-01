from .settings import *  # NOQA

import os.path

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, '..', 'kairly-client', 'dist', 'static')),
)

TEMPLATES[0]['DIRS'] = (
    os.path.abspath(os.path.join(BASE_DIR, '..', 'kairly-client', 'dist')),
)
