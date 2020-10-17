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

# at first perform dump working DB on local host
# python manage.py dumpdata > django_cinema/fixtures/db.json

#python manage.py shell --command="from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete(); exit()"
#python manage.py loaddata django_cinema/fixtures/db.json
#python manage.py captcha_clean
#python manage.py thumbnail_cleanup
#python manage.py clearsessions

python manage.py runserver 0.0.0.0:8000 --nostatic

exec "$@"