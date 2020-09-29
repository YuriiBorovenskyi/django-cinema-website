from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.template.loader import render_to_string

from beta_project.celery import celery_app

signer = Signer()


@celery_app.task
def send_activation_notification(user_id):
    """
    Function, that is called by 'user_registrated_dispatcher' signal handler.

    Send notification messages to current user with instructions for
    activation his account.

    This is celery task that will run in task queue (keeps in redis) and
    launch in background.
    """
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=user_id)

    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
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
