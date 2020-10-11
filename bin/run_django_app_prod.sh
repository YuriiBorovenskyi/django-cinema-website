#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
#python manage.py migrate
#python manage.py collectstatic --no-input --clear

# at first perform dump working DB on local host
# python manage.py dumpdata > cinema/fixtures/db.json

#python manage.py shell --command="from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete(); exit()"
#python manage.py loaddata cinema/fixtures/db.json
gunicorn django_cinema.wsgi:application --bind 0.0.0.0:8000

exec "$@"