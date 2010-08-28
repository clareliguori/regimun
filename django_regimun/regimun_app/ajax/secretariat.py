from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils import simplejson
from regimun_app.forms import jEditableForm, BasicConferenceInfoForm, \
    NewCommitteeForm, NewCountryForm
from regimun_app.models import Conference, Committee, Country
from regimun_app.views.secretariat_admin import secretariat_authenticate
import inspect
import string

@login_required
def conference_ajax_functions(request, conference_slug, func_name):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    func_name = string.replace(func_name, "-", "_")
    
    if secretariat_authenticate(request, conference) and func_name in globals() and inspect.isfunction(globals()[func_name]):
        return_value = globals()[func_name](request, conference)
        if return_value != None:
            if isinstance(return_value, HttpResponse):
                return return_value
            else:
                return HttpResponse(return_value, mimetype='application/javascript')
    
    raise Http404

def get_basic_conference_form(request, conference):
    form = BasicConferenceInfoForm(instance=conference)
    
    output = ""
    if conference.logo:
        output += "<img src=\"" + conference.logo.url + "\" border=\"0\" width=\"200\""
    output += "<form action=\"\" method=\"post\" id=\"basic_conference_info_form\"><table>"
    output += form.as_table()
    output += "</table></form>"
    return simplejson.dumps({'form':output})

def save_basic_conference_form(request, conference):
    form = BasicConferenceInfoForm(data=request.POST, instance=conference)
    
    if form.is_valid():
        conference = form.save()
        return HttpResponse()
    else:
        return simplejson.dumps({'form':form.as_p()})

def get_conference_committees(request, conference):
    existing_committees = serializers.serialize('json', Committee.objects.filter(conference=conference), fields=('name'))
    form = NewCommitteeForm()
    
    return simplejson.dumps({'form':form.as_p(), 'objects':existing_committees})

def get_conference_countries(request, conference):
    existing_countries = serializers.serialize('json', Country.objects.filter(conference=conference), fields=('name','flag_icon'))
    form = NewCountryForm()
    
    return simplejson.dumps({'form':form.as_p(), 'objects':existing_countries})

def edit_committee(request, conference):
    # clean the POST data
    if request.method == 'POST':
        form = jEditableForm(data=request.POST)
        if form.is_valid():
            # get the committee PK and attribute we want to set. The id is formatted "attr_pk"
            raw_id = request.POST.get('id', '')
            committee_attr, committee_pk = raw_id.rsplit("_")
            if committee_attr and committee_pk:
                committee = get_object_or_404(Committee, pk=committee_pk)
                value = form.cleaned_data['value']
                if committee.conference == conference and value:
                    committee.__setattr__(committee_attr, value)
                    committee.save()
                    return HttpResponse(value)

def remove_committee(request, conference):
    if request.method == 'POST':
        committee_pk = request.POST.get('pk', '')
        committee = get_object_or_404(Committee, pk=committee_pk)
        committee.delete()
        return simplejson.dumps({'pk':committee_pk})

def add_committee(request, conference):
    if request.method == 'POST':
        form = NewCommitteeForm(data=request.POST)
        if(form.is_valid()):
            committee = form.save(commit=False)
            committee.conference = conference
            committee.url_name = slugify(committee.name)
            committee.save()
            return simplejson.dumps({'pk':committee.pk, 'name':committee.name})
        else:
            return simplejson.dumps({'form':form.as_p()})
   
def edit_country(request, conference):
    # clean the POST data
    if request.method == 'POST':
        form = jEditableForm(data=request.POST)
        if form.is_valid():
            # get the country PK and attribute we want to set. The id is formatted "attr_pk"
            raw_id = request.POST.get('id', '')
            country_attr, country_pk = raw_id.rsplit("_")
            if country_attr and country_pk:
                country = get_object_or_404(Country, pk=country_pk)
                value = form.cleaned_data['value']
                if country.conference == conference and value:
                    country.__setattr__(country_attr, value)
                    country.save()
                    return HttpResponse(value)

def remove_country(request, conference):
    if request.method == 'POST':
        country_pk = request.POST.get('pk', '')
        country = get_object_or_404(Country, pk=country_pk)
        country.delete()
        return simplejson.dumps({'pk':country_pk})

def add_country(request, conference):
    if request.method == 'POST':
        form = NewCountryForm(data=request.POST)
        if(form.is_valid()):
            country = form.save(commit=False)
            country.conference = conference
            country.url_name = slugify(country.name)
            country.save()
            return simplejson.dumps({'pk':country.pk, 'name':country.name})
        else:
            return simplejson.dumps({'form':form.as_p()})
