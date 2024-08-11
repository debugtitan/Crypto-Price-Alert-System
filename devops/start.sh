#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

gunicorn config.wsgi:application --workers 3  --bind 0.0.0.0:8000 --timeout 0 --log-level info --access-logfile -