#!/bin/bash

. /srv/venv/bin/activate
export DJANGO_SETTINGS_MODULE=kairly.settings_prod
export PYTHONIOENCODING=utf-8
/srv/kairly/kairly-server/manage.py importtwitter -v 0
