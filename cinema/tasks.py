from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from django_cinema.celery import celery_app


@celery_app.task
def send_new_product_notification(product_id):
    """
    Function, that is called by 'post_save_dispatcher' signal handler.

    Send notification messages to registered users about appearance of new
    movie on blu-ray.

    This is celery task that will run in task queue (keeps in redis) and
    launch in background.
    """
    UserModel = get_user_model()
    users = UserModel.objects.exclude(email__endswith='hollywood.com')
    host = 'http://{0}'.format(
        settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else
        'localhost:8000'
    )
    for user in users:
        context = {
            'username': user.username, 'host': host, 'product_id': product_id
        }
        subject = render_to_string(
            'email/new_product_letter_subject.txt', context
        )
        body_text = render_to_string(
            'email/new_product_letter_body.txt', context
        )
        user.email_user(subject, body_text, fail_silently=False)
