#!/bin/sh

# wait for Redis and DB server to start
#sleep 10
#echo "HELLO"

python --command="from os.path import exists; log_file = 'logs/celery.log'; if not exists(log_file): with open(log_file, 'w') as f: pass"
celery worker --app=django_cinema --loglevel=info --logfile=logs/celery.log

exec "$@"