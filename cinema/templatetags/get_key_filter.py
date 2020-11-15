from django import template

register = template.Library()


@register.filter(name="get_key")
def get_key(dictionary, key):
    """Custom filter for getting value of variable-key in dictionary."""
    if key:
        return dictionary.get(key)
