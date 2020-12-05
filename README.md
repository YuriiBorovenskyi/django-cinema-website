[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# DjangoCinema: source code
Website of Cinema Library written in Django.
***
#### Include:

- Python
- Django
- PostgreSQL
- Celery
- Redis
- Django Rest Framework
- Gunicorn
- Nginx
- Docker
- Pytest
***
#### Database diagrams:

- db_diagram/short_diagram.svg
- db_diagram/full_diagram.svg
***
# Quick start
### I. Development
#### To run current project locally you need:

1. Requirements:
    - *'.env.dev'* file with environment variables
    - *'.env.dev.db'* file with DB environment variables
2. Start by cloning down this project from **GitHub** repository.
3. Set up **Python** development environment.
4. Install **Docker** / **Docker-compose**.
5. Run `docker-compose up -d --build`.
6. Run `docker exec -it django_web python manage.py flush --no-input`.
7. Run `docker exec -it django_web python manage.py migrate`.
8. Run `docker exec -it django_web python manage.py shell --command="from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete(); exit()"`.
9. Run `docker exec -it django_web python manage.py loaddata django_cinema/fixtures/db.json`.
10. Open browser at <http://localhost:8000/> to visit website.

***
### II. Production
#### To deploy current project to Amazon Web Services (AWS) EC2 you need:

1. Configure **Virtual Private Cloud** (VPC) for your account:
    - Create AWS account
    - Set up new EC2 instance
    - Configure AWS Security Group
    - Configure SSH-access into EC2 using Key Pair
    - Connect local machine to EC2 via SSH
    - Configure and use an Elastic IP address
    - Set up an IAM role
    - Create Amazon S3 bucket, configure IAM user and group to store and serve up static and media files
    - Install and configure AWS CLI using your access key and secret key getting early
2. Requirements:
    - *'.env.prod'* file with environment variables;
    - *'.env.prod.db'* file with DB environment variables;
3. Start by cloning down this project from **GitHub** repository to EC2.
4. Install **Docker** / **Docker-compose** on EC2.
5. Run `docker-compose -f docker-compose.prod.yml up -d --build`.
6. Run `docker exec -it django_web python manage.py flush --no-input`.
7. Run `docker exec -it django_web python manage.py migrate`.
8. Load static files from EC2 to **Amazon S3** bucket:
    - run `docker exec -it django_web python manage.py collectstatic --no-input --clear`
9. Run `docker exec -it django_web python manage.py shell --command="from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete(); exit()"`.
10. Run `docker exec -it django_web python manage.py loaddata django_cinema/fixtures/db.json`.
11. Load media files from EC2 to **Amazon S3** bucket:
    - run `aws s3 sync media s3://<your_bucket_name>/media --exclude *.tmp`
12. Open browser at <http://13.49.215.150:80/> to visit website.
