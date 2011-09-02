from django import template

register = template.Library()

@register.filter
def is_secretariat_member(user):
    try:
        return user.secretariat_member != None and user.secretariat_member.conferences != None
    except:
        return False

@register.filter
def is_faculty_sponsor(user):
    try:
        return user.faculty_sponsor != None and user.faculty_sponsor.school != None
    except:
        return False

@register.filter
def is_not_secretariat_member(user):
    return not is_secretariat_member(user)

@register.filter
def is_not_faculty_sponsor(user):
    return not is_faculty_sponsor(user)
