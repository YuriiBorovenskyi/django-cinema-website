from django.conf import settings
from django.template.loader import render_to_string

from accounts.models import User

users = User.objects.exclude(email__endswith='hollywood.com')


def send_new_product_notification(product):
    """
    Function, that is called by 'post_save_dispatcher' signal handler.

    Send notification messages to registered users about appearance of new
    movie on blu-ray.
    """
    host = 'http://{0}'.format(
        settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else
        'localhost:8000'
    )
    for user in users:
        context = {'user': user, 'host': host, 'product': product}
        subject = render_to_string(
            'email/new_product_letter_subject.txt', context
        )
        body_text = render_to_string(
            'email/new_product_letter_body.txt', context
        )
        user.email_user(subject, body_text, fail_silently=True)
