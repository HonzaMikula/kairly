#!/bin/bash

. /srv/venv/bin/activate
export DJANGO_SETTINGS_MODULE=kairly.settings_cron_prod
export PYTHONIOENCODING=utf-8
/srv/kairly/server/manage.py addfreecredits --all -v 0
