from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal

from .tasks import send_activation_notification


class User(AbstractUser):
    """Custom 'User' Model.

    It uses user authentication system of Django. Class of this model
    inherits from standard 'AbstractUser' class.
    """

    email = models.EmailField(unique=True, verbose_name="Email address")

    class Meta:
        db_table = "auth_user"
        ordering = ["first_name", "last_name"]


user_registrated = Signal(providing_args=["instance"])


def user_registrated_dispatcher(sender, instance, **kwargs):
    """Signal handler function.

    After saving record of 'User' model in database, 'user_registrated' signal
    will be send, which calls this signal handler.
    Call  function, that sends notification messages to current user with
    instructions for activation his account.

    'send_activation_notification' is celery task that will run in task
    queue (keeps in redis) and launch in background.
    """
    send_activation_notification.delay(instance.pk)


user_registrated.connect(user_registrated_dispatcher)
