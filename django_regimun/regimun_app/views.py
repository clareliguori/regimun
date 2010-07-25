from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from recaptcha.client import captcha
from regimun_app.forms import NewSchoolForm, NewFacultySponsorForm, \
    ConferenceForm, SecretariatUserForm
from regimun_app.models import Conference, School, FacultySponsor, Country, \
    Committee, Secretariat
from settings import MEDIA_ROOT
import csv

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

@login_required
def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_response(request, 'regimun_app/school/index.html', {'conference' : conference, 'school' : school})

def validate_newsponsor_form(sponsor_form):
    if sponsor_form.is_valid():
        username = sponsor_form.cleaned_data['sponsor_username']
        if username:
            if User.objects.filter(username=username).count():
                sponsor_form._errors.setdefault("sponsor_username", ErrorList()).append(u"Username is not available.")
                return False
            return True
    
    return False

def validate_newschool_form(school_form, conference_slug):
    if school_form.is_valid():
        schoolname = school_form.cleaned_data['school_name']
        if schoolname and conference_slug:
            if School.objects.filter(name=schoolname, conference__url_name=conference_slug).count():
                school_form._errors.setdefault("school_name", ErrorList()).append(u"School name is not available.")
                return False
            return True

    return False

def get_recaptcha_response(request):
    captcha_response = \
    captcha.submit(request.POST.get("recaptcha_challenge_field", None),
                   request.POST.get("recaptcha_response_field", None),
                   "6LeeursSAAAAAAsPzg0VPYpkfP9lbtXL9Bmeysh-",
                   request.META.get("REMOTE_ADDR", None))
        
    return captcha_response

def create_school(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if request.method == 'POST': 
        school_form = NewSchoolForm(request.POST)
        sponsor_form = NewFacultySponsorForm(request.POST)
        captcha_response = get_recaptcha_response(request)
        
        if validate_newschool_form(school_form, conference_slug) and validate_newsponsor_form(sponsor_form):
            if captcha_response.is_valid:
                new_school = School()
                new_school.conference = conference
                new_school.name = school_form.cleaned_data['school_name']
                new_school.url_name = slugify(school_form.cleaned_data['school_name'])
                new_school.address_line_1 = school_form.cleaned_data['school_address_line_1']
                new_school.address_line_2 = school_form.cleaned_data['school_address_line_2']
                new_school.city = school_form.cleaned_data['school_city']
                new_school.state = school_form.cleaned_data['school_state']
                new_school.zip = school_form.cleaned_data['school_zip']
                new_school.address_country = school_form.cleaned_data['school_address_country']
                new_school.save()
    
                new_user = User()
                new_user.username = sponsor_form.cleaned_data['sponsor_username']
                new_user.first_name = sponsor_form.cleaned_data['sponsor_first_name']
                new_user.last_name = sponsor_form.cleaned_data['sponsor_last_name']
                new_user.email = sponsor_form.cleaned_data['sponsor_email']
                new_user.username = sponsor_form.cleaned_data['sponsor_username']
                new_user.set_password(sponsor_form.cleaned_data['sponsor_password'])
                new_user.save()
    
                new_sponsor = FacultySponsor()
                new_sponsor.user = new_user
                new_sponsor.school = new_school
                new_sponsor.phone = sponsor_form.cleaned_data['sponsor_phone']
                new_sponsor.save()
    
                return HttpResponseRedirect(reverse('django_regimun.regimun_app.views.school_created', 
                                                    args=(conference.url_name,new_school.url_name,)))
            else:
                school_form._errors.setdefault("school_name", ErrorList()).append(captcha_response.error_code)

    else:
        school_form = NewSchoolForm()
        sponsor_form = NewFacultySponsorForm()

    return render_response(request, 'regimun_app/register-new-school.html', {
        'school_form': school_form, 'sponsor_form': sponsor_form, 'conference' : conference
    })

def school_created(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_response(request, 'regimun_app/school/school-created.html', {'conference' : conference, 'school' : school})

def create_conference(request):
    if request.method == 'POST': 
        conference_form = ConferenceForm(request.POST)
        user_form = SecretariatUserForm(request.POST)
        
        if conference_form.is_valid() and user_form.is_valid():
            new_conference = conference_form.save(commit=False)
            new_conference.url_name = slugify(conference_form.cleaned_data['name'])
            new_conference.save()
            
            # create default countries
            defaultCountriesList = MEDIA_ROOT + "default_countries/default_countries.csv"
            countriesListReader = csv.reader(open(defaultCountriesList))
            for row in countriesListReader:
                new_country = Country()
                new_country.conference = new_conference
                new_country.name = row[0]
                new_country.url_name = slugify(new_country.name)
                new_country.flag_icon = "default_countries/icons/" + row[1]
                new_country.save()
                
            # create default committees and delegate positions
            defaultCommitteesList = MEDIA_ROOT + "default_committees.csv"
            committeesListReader = csv.reader(open(defaultCommitteesList))
            for row in committeesListReader:
                new_committee = Committee()
                new_committee.conference = new_conference
                new_committee.name = row[0]
                new_committee.url_name = slugify(new_committee.name)
                new_committee.save()
            
            user = user_form.save()
            secretariat_user = Secretariat()
            secretariat_user.user = user
            secretariat_user.conference = new_conference
            secretariat_user.save()
            
            return HttpResponseRedirect(reverse('django_regimun.regimun_app.views.conference_created', 
                                                args=(new_conference.url_name,)))
    else:
        conference_form = ConferenceForm()
        user_form = SecretariatUserForm()

    return render_response(request, 'regimun_app/conference/create-conference.html', {
        'conference_form': conference_form, 'secretariat_form' : user_form
    })

def conference_created(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    return render_response(request, 'regimun_app/conference/conference-created.html', {'conference' : conference,})
    