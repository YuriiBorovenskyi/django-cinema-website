import os

log_file_path = 'logs/celery.log'
dir_name = os.path.dirname(log_file_path)

if not os.path.isdir(dir_name):
    os.mkdir(dir_name)

if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        pass
