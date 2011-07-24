from django import template
from django.utils.translation import to_locale, get_language
import locale

locale.setlocale(locale.LC_ALL, '')
register = template.Library()

@register.filter
def currencyformat (value): 
    print to_locale(get_language())
    return locale.currency(float(value), grouping=True)
