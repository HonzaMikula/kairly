#!/bin/bash

. /srv/venv/bin/activate
export DJANGO_SETTINGS_MODULE=kairly.settings_prod
export PYTHONIOENCODING=utf-8
/srv/app/manage.py importrss
