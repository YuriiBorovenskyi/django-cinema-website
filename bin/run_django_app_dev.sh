#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# TODO: After website development finishing, you need to make following steps:
# TODO: 1. Delete unnecessary and unimportant data from database.
# - run 'python manage.py captcha_clean'
# - run 'python manage.py thumbnail_cleanup'
# - run 'python manage.py clearsessions'
# TODO: 2. Make backup (export) of entire database.
# - run 'python manage.py dumpdata > django_cinema/fixtures/db.json'

python manage.py runserver 0.0.0.0:8000 --nostatic

exec "$@"