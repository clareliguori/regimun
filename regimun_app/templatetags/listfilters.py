from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter
def in_list(value, arg):
    try:
        arg.get(id=value.id)
        return True
    except ObjectDoesNotExist:
        return False

@register.filter
def not_in_list(value, arg):
    try:
        arg.get(id=value.id)
        return False
    except ObjectDoesNotExist:
        return True
