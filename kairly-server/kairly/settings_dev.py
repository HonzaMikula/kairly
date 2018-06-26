from .settings import *  # NOQA

import os.path

# Unused for now, just use node dev server on :8080 for frontend endpoitns

MEDIA_URL = 'http://localhost:8000/media/'

# STATICFILES_DIRS = (
#     os.path.abspath(os.path.join(BASE_DIR, '..', 'kairly-client', 'dist', 'static')),
# )
#
# TEMPLATES[0]['DIRS'] = (
#     os.path.abspath(os.path.join(BASE_DIR, '..', 'kairly-client', 'dist')),
# )
