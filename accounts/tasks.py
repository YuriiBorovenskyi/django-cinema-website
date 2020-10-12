import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.template.loader import render_to_string

from django_cinema.celery import celery_app

signer = Signer()

LOGGER = logging.getLogger(__name__)


@celery_app.task
def send_activation_notification(user_id):
    """
    Function, that is called by 'user_registrated_dispatcher' signal handler.

    Send notification message to current user with instruction for
    activation his account.

    This is celery task that will run in task queue (keeps in redis) and
    launch in background.
    """
    LOGGER.info("Run celery task - Send activation notification.")

    UserModel = get_user_model()
    user = UserModel.objects.get(pk=user_id)
    ip = settings.ALLOWED_HOSTS[0]
    if not settings.DEBUG:
        port = 80
    else:
        port = 8000
    host = f'http://{ip}:{port}'
    context = {
        'username': user.username,
        'host': host,
        'sign': signer.sign(user.username)
    }
    subject = render_to_string(
        'email/activation_letter_subject.txt', context
    )
    body_text = render_to_string(
        'email/activation_letter_body.txt', context
    )
    user.email_user(subject, body_text)

    LOGGER.info(f"Sent message to {user.username}'s e-mail with instruction "
                f"for activation his account.")
