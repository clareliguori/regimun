from dajax.core.Dajax import Dajax
from django.template.defaultfilters import slugify
from django.utils import simplejson

def get_school_mailing_address_form(request, school_pk):
    from regimun_app.models import School
    from regimun_app.forms import SchoolMailingAddressForm
    school = School.objects.get(pk=school_pk)
    form = SchoolMailingAddressForm(instance=school)
    return simplejson.dumps({'form':form.as_p()})

def save_school_mailing_address_form(request, school_pk, form):
    from regimun_app.models import School
    from regimun_app.forms import SchoolMailingAddressForm
    
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
            dajax.add_css_class('#school_mailing_address_form #id_%s' % error,'error')
    return dajax.json()

def get_edit_sponsor_form(request, sponsor_pk):
    from regimun_app.models import FacultySponsor
    from regimun_app.forms import EditFacultySponsorForm

    sponsor = FacultySponsor.objects.get(pk=sponsor_pk)
    form = EditFacultySponsorForm(initial={'sponsor_first_name': sponsor.user.first_name, 'sponsor_last_name':sponsor.user.last_name,'sponsor_email':sponsor.user.email,'sponsor_phone':sponsor.phone})
    return simplejson.dumps({'form':form.as_p(), 'sponsor_pk':sponsor_pk})

def save_edit_sponsor_form(request, sponsor_pk, form):
    from regimun_app.models import FacultySponsor
    from regimun_app.forms import EditFacultySponsorForm
    
    dajax = Dajax()
    sponsor = FacultySponsor.objects.get(pk=sponsor_pk)
    form = EditFacultySponsorForm(form)
    
    if form.is_valid():
        sponsor.user.first_name = form.cleaned_data['sponsor_first_name']
        sponsor.user.last_name = form.cleaned_data['sponsor_last_name']
        sponsor.user.email = form.cleaned_data['sponsor_email']
        sponsor.phone = form.cleaned_data['sponsor_phone']
        sponsor.save()
        
        dajax.remove_css_class('#sponsor_form_' + str(sponsor_pk) + ' input','error')
        data = dict(username=sponsor.user.username, sponsor_id=sponsor_pk, full_name=sponsor.user.get_full_name(), email=sponsor.user.email, phone=sponsor.phone)
        dajax.add_data(data, 'updated_sponsor_data')
    else:
        dajax.remove_css_class('#sponsor_form_' + str(sponsor_pk) + ' input','error')
        for error in form.errors:
            print error
            dajax.add_css_class('#sponsor_form_' + str(sponsor_pk) + ' #id_%s' % error,'error')
    return dajax.json()

def remove_sponsor(request, sponsor_pk):
    from regimun_app.models import FacultySponsor

    sponsor = FacultySponsor.objects.get(pk=sponsor_pk)
    sponsor.delete()
    
    dajax = Dajax()
    dajax.remove('#sponsor_'+str(sponsor_pk))
    dajax.remove('#buttons_sponsor_'+str(sponsor_pk))
    return dajax.json()

def get_basic_conference_form(request, conference_pk):
    from regimun_app.models import Conference
    from regimun_app.forms import BasicConferenceInfoForm

    conference = Conference.objects.get(pk=conference_pk)
    form = BasicConferenceInfoForm(instance=conference)
    
    dajax = Dajax()
    output = "<form action=\"\" method=\"post\" id=\"basic_conference_info_form\">";
    output += form.as_p()
    output += "</form>"
    dajax.assign('#basic-conference-form-dialog','innerHTML',output)
    return dajax.json()

def save_basic_conference_form(request, conference_pk, form):
    from regimun_app.models import Conference
    from regimun_app.forms import BasicConferenceInfoForm
    
    dajax = Dajax()
    conference = Conference.objects.get(pk=conference_pk)
    form = BasicConferenceInfoForm(form, instance=conference)
    
    if form.is_valid():
        conference = form.save()
    else:
        dajax.remove_css_class('#basic_conference_info_form input','error')
        for error in form.errors:
            print error
            dajax.add_css_class('#basic_conference_info_form #id_%s' % error,'error')
    return dajax.json()

def get_conference_countries_formset(request, conference_pk):
    from regimun_app.models import Conference, Country
    from regimun_app.forms import CountryFormSet

    conference = Conference.objects.get(pk=conference_pk)
    formset = CountryFormSet(queryset=Country.objects.filter(conference=conference))

    dajax = Dajax()
    output = "<form action=\"\" method=\"post\" id=\"conference_countries_form\"><table>";
    output += formset.as_table()
    output += "</table></form>"
    dajax.assign('#countries-form-dialog','innerHTML',output)
    return dajax.json()

def save_conference_countries_formset(request, conference_pk, form):
    from regimun_app.models import Conference
    from regimun_app.forms import CountryFormSet
    
    dajax = Dajax()
    conference = Conference.objects.get(pk=conference_pk)
    formset = CountryFormSet(form)
    
    if formset.is_valid():
        countries = formset.save(commit=False)
        for country in countries:
            if country.name and not country.url_name:   # new country
                country.url_name = slugify(country.name)
                country.conference = conference
            if country.name:
                country.save()
    else:
        dajax.remove_css_class('#conference_countries_form input','error')
        for error in formset.errors:
            print error
            dajax.add_css_class('#conference_countries_form #id_%s' % error,'error')
    return dajax.json()

def get_conference_committees_formset(request, conference_pk):
    from regimun_app.models import Conference, Committee
    from regimun_app.forms import CommitteeFormSet

    conference = Conference.objects.get(pk=conference_pk)
    formset = CommitteeFormSet(queryset=Committee.objects.filter(conference=conference))

    dajax = Dajax()
    output = "<form action=\"\" method=\"post\" id=\"conference_committees_form\"><table>";
    output += formset.as_table()
    output += "</table></form>"
    dajax.assign('#committees-form-dialog','innerHTML',output)
    return dajax.json()

def save_conference_committees_formset(request, conference_pk, form):
    from regimun_app.models import Conference
    from regimun_app.forms import CommitteeFormSet
    
    dajax = Dajax()
    conference = Conference.objects.get(pk=conference_pk)
    formset = CommitteeFormSet(form)
    
    if formset.is_valid():
        committees = formset.save(commit=False)
        for committee in committees:
            if committee.name and not committee.url_name:   # new committee
                committee.url_name = slugify(committee.name)
                committee.conference = conference
            if committee.name:
                committee.save()
    else:
        dajax.remove_css_class('#conference_committees_form input','error')
        for error in formset.errors:
            print error
            dajax.add_css_class('#conference_committees_form #id_%s' % error,'error')
    return dajax.json()
