from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal

from .utilities import send_activation_notification


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email address')
    # is_activated = models.BooleanField(
    #     default=True, db_index=True, verbose_name='Activated?'
    # )
    # send_messages = models.BooleanField(
    #     default=True, verbose_name='Send notifications about new comments?'
    # )

    class Meta:
        db_table = 'auth_user'
        ordering = ["first_name", "last_name"]


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)
