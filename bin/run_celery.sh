#!/bin/sh

# wait for Redis and DB server to start
#sleep 10
#echo "HELLO"

python create_celery_log_if_not.py
celery worker --app=django_cinema --loglevel=info --logfile=logs/celery.log

exec "$@"