from django.conf import settings
from django.template.loader import render_to_string

from accounts.forms import users


def send_new_product_notification(product):
    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    for user in users:
        context = {'user': user, 'host': host, 'product': product}
        subject = render_to_string(
            'email/new_product_letter_subject.txt', context
        )
        body_text = render_to_string(
            'email/new_product_letter_body.txt', context
        )
        user.email_user(subject, body_text, fail_silently=True)
