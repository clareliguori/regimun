from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from regimun_app.forms import NewSchoolForm, NewFacultySponsorForm
from regimun_app.models import Conference, School, FacultySponsor, Committee, \
    DelegatePosition, Country
from regimun_app.utils import fetch_resources
from regimun_app.views.general import render_response, get_recaptcha_response
import cStringIO as StringIO
import csv
import ho.pisa as pisa
import re
import settings

def school_authenticate(request, conference, school):
    if school.conference != conference:
        return False
    
    if request.user.is_staff:
        return True
    
    try:
        return request.user.secretariat_member.conference.pk == conference.pk
    except ObjectDoesNotExist:
        pass
    
    try:
        return request.user.faculty_sponsor.school.pk == school.pk
    except ObjectDoesNotExist:
        return False

@login_required
def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_response(request, 'school/index.html', {'conference' : conference, 'school' : school})

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
            if School.objects.filter(name=schoolname, conference__url_name=conference_slug).count() or slugify(schoolname) == "secretariat":
                school_form._errors.setdefault("school_name", ErrorList()).append(u"School name is not available.")
                return False
            return True

    return False

def create_school(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if request.method == 'POST': 
        school_form = NewSchoolForm(request.POST)
        sponsor_form = NewFacultySponsorForm(request.POST)
        captcha_response = get_recaptcha_response(request)
        
        if validate_newschool_form(school_form, conference_slug):
            if request.user.is_authenticated() or validate_newsponsor_form(sponsor_form):
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
                    new_school.access_code = User.objects.make_random_password()
                    new_school.save()
        
                    new_sponsor = FacultySponsor()
                    new_sponsor.school = new_school
                    if hasattr(sponsor_form,'cleaned_data'):
                        new_sponsor.phone = sponsor_form.cleaned_data['sponsor_phone']
                    
                    new_user = request.user
                    if not request.user.is_authenticated():
                        new_user = User()
                        new_user.username = sponsor_form.cleaned_data['sponsor_username']
                        new_user.first_name = sponsor_form.cleaned_data['sponsor_first_name']
                        new_user.last_name = sponsor_form.cleaned_data['sponsor_last_name']
                        new_user.email = sponsor_form.cleaned_data['sponsor_email']
                        new_user.username = sponsor_form.cleaned_data['sponsor_username']
                        new_user.set_password(sponsor_form.cleaned_data['sponsor_password'])
                        new_user.save()
                    else:
                        try:
                            # delete any existing faculty sponsor ties
                            existing_sponsor = FacultySponsor.objects.get(user=new_user)
                            new_sponsor.phone = existing_sponsor.phone
                            existing_sponsor.delete()
                        except ObjectDoesNotExist:
                            pass
                    
                    new_sponsor.user = new_user
                    new_sponsor.save()
        
                    return HttpResponseRedirect(reverse(school_admin, 
                                                        args=(conference.url_name,new_school.url_name,)))
                else:
                    school_form._errors.setdefault("school_name", ErrorList()).append("The reCAPTCHA wasn't entered correctly.")

    else:
        school_form = NewSchoolForm()
        sponsor_form = NewFacultySponsorForm()

    return render_response(request, 'register-new-school.html', {
        'school_form': school_form, 'sponsor_form': sponsor_form, 'conference' : conference
    })

def grant_school_access(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)

    if request.method == 'POST':
        access_code = request.POST.get("access_code","")
        redirect_to = request.POST.get("next", '')
        if access_code == school.access_code:
            # grant access to this school
            sponsor = FacultySponsor()
            sponsor.user = request.user
            sponsor.school = school
            sponsor.save()

            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            return HttpResponseRedirect(redirect_to)

    return render_response(request, "school/wrong-access-code.html", {'conference' : conference, 'school' : school})

@login_required
def generate_invoice(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
 
    if school_authenticate(request, conference, school):
        context_dict = {
        'pagesize' : 'letter',
        'conference' : conference,
        'school' : school, }
        html = render_to_string('school/invoice.html', context_dict, context_instance=RequestContext(request))
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
        if not pdf.err:
            response = http.HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=invoice-' + conference_slug + "-" + school_slug + '.pdf'
            return response
        else:
            raise Http404
    else:
        raise Http404

@login_required
def generate_request_based_invoice(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)

    if school_authenticate(request, conference, school):
        context_dict = {
            'pagesize' : 'letter',
            'conference' : conference,
            'school' : school, }
        html = render_to_string('school/invoice-from-request.html', context_dict, context_instance=RequestContext(request))
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
        if not pdf.err:
            response = http.HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=invoice-' + conference_slug + "-" + school_slug + '.pdf'
            return response
        else:
            raise Http404
    else:
        raise Http404                                                                                       

@login_required
def school_spreadsheet_downloads(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    
    if school_authenticate(request, conference, school):
        response = HttpResponse(mimetype='text/csv')
        writer = csv.writer(response)
        
        if 'country-committee-assignments' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=country-committee-assignments-' + conference_slug + ".csv"             
            committees = Committee.objects.filter(conference=conference)
            countries = Country.objects.filter(conference=conference)
    
            headers = ['Country']
            for committee in committees:
                headers.append(committee.name)
            writer.writerow(headers)

            for country in countries:
                row = [country.name]
                for committee in committees:
                    row.append(str(DelegatePosition.objects.filter(committee=committee,country=country).count()))
                writer.writerow(row)
        else:
            raise Http404
    else:
        raise Http404
    return response

@login_required
def get_fees_table(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    
    if school_authenticate(request, conference, school):
        return render_response(request, 'school/fees.html', {'conference' : conference, 'school' : school})
    raise Http404
