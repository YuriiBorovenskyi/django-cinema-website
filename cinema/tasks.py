import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from django_cinema.celery import celery_app

LOGGER = logging.getLogger(__name__)


@celery_app.task
def send_new_product_notification(product_id):
    """Function, that is called by 'post_save_dispatcher' signal handler.

    Send notification messages to registered users about appearance of new
    movie on blu-ray.

    This is celery task that will run in task queue (keeps in redis) and
    launch in background.
    """
    LOGGER.info("Run celery task - Send new product notification.")

    UserModel = get_user_model()
    users = UserModel.objects.exclude(email__endswith="hollywood.com")
    ip = settings.ALLOWED_HOSTS[0]
    if not settings.DEBUG:
        port = 80
    else:
        port = 8000
    host = f"http://{ip}:{port}"
    for user in users:
        context = {
            "username": user.username,
            "host": host,
            "product_id": product_id,
        }
        subject = render_to_string(
            "email/new_product_letter_subject.txt", context
        )
        body_text = render_to_string(
            "email/new_product_letter_body.txt", context
        )
        user.email_user(subject, body_text, fail_silently=False)

        LOGGER.info(
            f"Sent message to {user.username}'s e-mail about "
            f"appearance of new movie on blu-ray."
        )
