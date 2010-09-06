from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from regimun_app.forms import SchoolMailingAddressForm, EditFacultySponsorForm
from regimun_app.models import Conference, School, FacultySponsor
from regimun_app.views.school_admin import school_authenticate
import inspect
import string

@login_required
def school_ajax_functions(request, conference_slug, school_slug, func_name):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    func_name = string.replace(func_name, "-", "_")
    
    if school_authenticate(request, conference, school) and func_name in globals() and inspect.isfunction(globals()[func_name]):
        return_value = globals()[func_name](request, school)
        if return_value != None:
            if isinstance(return_value, HttpResponse):
                return return_value
            else:
                return HttpResponse(return_value, mimetype='application/javascript')
    
    raise Http404

def get_school_mailing_address_form(request, school):
    form = SchoolMailingAddressForm(instance=school)
    return simplejson.dumps({'form':form.as_p()})

def save_school_mailing_address_form(request, school):
    form = SchoolMailingAddressForm(data=request.POST, instance=school)
    
    if form.is_valid():
        school = form.save()
        return simplejson.dumps({'new_school_mailing_address': school.get_html_mailing_address()})
    else:
        return simplejson.dumps({'form':form.as_p()})

def get_edit_sponsor_form(request, school):
    if request.method == 'POST':
        sponsor_pk = request.POST.get('sponsor_pk','')
        sponsor = get_object_or_404(FacultySponsor, pk=sponsor_pk)
        if sponsor.school == school:
            form = EditFacultySponsorForm(initial={'sponsor_pk':sponsor_pk, 'sponsor_first_name': sponsor.user.first_name, 'sponsor_last_name':sponsor.user.last_name,'sponsor_email':sponsor.user.email,'sponsor_phone':sponsor.phone})
            return simplejson.dumps({'form':form.as_p(), 'sponsor_pk':sponsor_pk})

def save_edit_sponsor_form(request, school):
    if request.method == 'POST':
        form = EditFacultySponsorForm(data=request.POST)
    
        if form.is_valid():
            sponsor_pk = form.cleaned_data['sponsor_pk']
            sponsor = get_object_or_404(FacultySponsor, pk=sponsor_pk)
            if sponsor.school == school:
                sponsor.user.first_name = form.cleaned_data['sponsor_first_name']
                sponsor.user.last_name = form.cleaned_data['sponsor_last_name']
                sponsor.user.email = form.cleaned_data['sponsor_email']
                sponsor.phone = form.cleaned_data['sponsor_phone']
                sponsor.save()
        
                data = dict(username=sponsor.user.username, sponsor_pk=str(sponsor_pk), full_name=sponsor.user.get_full_name(), email=sponsor.user.email, phone=sponsor.phone)        
                return simplejson.dumps(data)
        else:
            return simplejson.dumps({'form':form.as_p(), 'sponsor_pk':sponsor_pk})

def remove_sponsor(request, school):
    if request.method == 'POST':
        sponsor_pk = request.POST.get('sponsor_pk','')
        sponsor = get_object_or_404(FacultySponsor, pk=sponsor_pk)
        if sponsor.school == school:
            sponsor.delete()
            return simplejson.dumps({'success':'true', 'sponsor_pk':sponsor_pk})
    