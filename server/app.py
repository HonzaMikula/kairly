import os

# Pokud se settings nachazí v /srv/app/moje_aplikace,
# bude obsah pro DJANGO_SETTINGS_MODULE: moje_aplikace.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kairly.settings_prod")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
