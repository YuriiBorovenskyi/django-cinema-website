import os

LOG_FILE_PATH = "logs/celery.log"
dir_name = os.path.dirname(LOG_FILE_PATH)

if not os.path.isdir(dir_name):
    os.mkdir(dir_name)

if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w") as f:
        pass
