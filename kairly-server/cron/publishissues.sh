#!/bin/bash

. /srv/venv/bin/activate
export DJANGO_SETTINGS_MODULE=kairly.settings_prod
/srv/app/manage.py publishissues
