from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def setting (name): 
    return str(settings.__getattr__(name))
