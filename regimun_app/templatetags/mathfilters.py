from django import template

register = template.Library()

def mult(value, arg):
    "Multiplies the arg and the value"
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0
mult.is_safe = True

def sub(value, arg):
    "Subtracts the arg from the value"
    try:
        return float(value) - float(arg)
    except ValueError:
        return 0
sub.is_safe = True

def div(value, arg):
    "Divides the value by the arg"
    try:
        return float(value) / float(arg)
    except ValueError:
        return 0
div.is_safe = True

register.filter('mult', mult)
register.filter('sub', sub)
register.filter('div', div)
