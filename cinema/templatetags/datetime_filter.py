from django import template

register = template.Library()


@register.filter(name='format_datetime')
def format_datetime(value):
    """
    The custom filter for formatting django-field 'Duration'.
    """
    hours, rem = divmod(value.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f'{hours}h {minutes}min'
