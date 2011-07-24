from django import template
import locale

locale.setlocale(locale.LC_ALL, '')
register = template.Library()

@register.filter
def currencyformat (value): 
    return locale.currency(float(value), grouping=True)
