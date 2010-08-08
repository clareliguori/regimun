from dajax.core.Dajax import Dajax
from dajaxice.core import dajaxice_functions
from django.utils import simplejson

def get_school_mailing_address_form(request, school_pk):
    from regimun_app.models import School
    from forms import SchoolMailingAddressForm

    school = School.objects.get(pk=school_pk)
    form = SchoolMailingAddressForm(instance=school)
    return simplejson.dumps({'form':form.as_p()})

dajaxice_functions.register(get_school_mailing_address_form)

def save_school_mailing_address_form(request, school_pk, form):
    from regimun_app.models import School
    from forms import SchoolMailingAddressForm
    
    dajax = Dajax()
    school = School.objects.get(pk=school_pk)
    form = SchoolMailingAddressForm(form, instance=school)
    
    if form.is_valid():
        school = form.save()
        dajax.remove_css_class('#school_mailing_address_form input','error')
        dajax.add_data(school.get_html_mailing_address(), 'new_school_mailing_address')
    else:
        dajax.remove_css_class('#school_mailing_address_form input','error')
        for error in form.errors:
            print error
            dajax.add_css_class('#id_%s' % error,'error')
    return dajax.json()

dajaxice_functions.register(save_school_mailing_address_form)
