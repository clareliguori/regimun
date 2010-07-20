from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from regimun_app.forms import NewSchoolForm, NewFacultySponsorForm
from regimun_app.models import Conference, School, FacultySponsor

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

@login_required
def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_response(request, 'regimun_app/school/index.html', {'conference' : conference, 'school' : school})

def school_created(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_response(request, 'regimun_app/school/school_created.html', {'conference' : conference, 'school' : school})

def create_school(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if request.method == 'POST': 
        school_form = NewSchoolForm(request.POST)
        sponsor_form = NewFacultySponsorForm(request.POST)
        if school_form.is_valid() and sponsor_form.is_valid():
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
        school_form = NewSchoolForm()
        sponsor_form = NewFacultySponsorForm()

    return render_response(request, 'regimun_app/register-new-school.html', {
        'school_form': school_form, 'sponsor_form': sponsor_form, 'conference' : conference
    })
    