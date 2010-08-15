from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from regimun_app.forms import ConferenceForm, SecretariatUserForm, \
    SchoolNameForm
from regimun_app.models import Conference, FacultySponsor, Delegate, Country, \
    Committee, Secretariat, School
from regimun_app.views.general import render_response
from regimun_app.views.school_admin import school_admin
from reportlab.pdfgen import canvas
from settings import MEDIA_ROOT
import csv

def secretariat_authenticate(request, conference):
    if request.user.is_staff:
        return True
    try:
        return request.user.secretariat_member.conference.pk == conference.pk
    except ObjectDoesNotExist:
        return False

@login_required
def spreadsheet_downloads(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if secretariat_authenticate(request, conference):
        response = HttpResponse(mimetype='text/csv')
        writer = csv.writer(response)
        
        if 'sponsor-contacts' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=sponsor-contacts-' + conference_slug + ".csv"            
            writer.writerow(['School', 'First Name', 'Last Name', 'E-mail Address', 'Phone',
                            'Street Address','Address 2','City','State / Province / Region','ZIP / Postal Code','Country'])
            
            sponsors = FacultySponsor.objects.select_related().filter(school__conference__url_name__exact=conference_slug)
            
            for sponsor in sponsors:
                school = sponsor.school
                writer.writerow([school.name,
                                 sponsor.user.first_name, sponsor.user.last_name, sponsor.user.email, sponsor.phone,
                                 school.address_line_1, school.address_line_2, school.city, school.state, school.zip, school.address_country])
             
        elif 'delegates' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=delegates-' + conference_slug + ".csv" 
            writer.writerow(['School', 'Country', 'Committee', 'Title', 'First Name', 'Last Name'])
            
            delegates = Delegate.objects.select_related().filter(position_assignment__country__conference__url_name__exact=conference_slug)
            
            for delegate in delegates:
                writer.writerow([delegate.position_assignment.school.name, delegate.position_assignment.country.name,
                                 delegate.position_assignment.committee.name, delegate.position_assignment.title, 
                                 delegate.first_name, delegate.last_name])
            
        elif 'school-country-assignments' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=school-country-assignments-' + conference_slug + ".csv" 
        elif 'country-committee-assignments' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=country-committee-assignments-' + conference_slug + ".csv"             
        else:
            raise Http404
    else:
        raise Http404
    return response

@login_required
def generate_all_invoices(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    
    if secretariat_authenticate(request, conference):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=invoices-' + conference_slug + '.pdf'
        p = canvas.Canvas(response)
    
        for school in conference.school_set.all():
            # Draw things on the PDF
            p.drawString(100, 100, conference.name + " INVOICE : " + school.name)
            p.showPage()
            
        p.save()
        return response
    else:
        raise Http404

@login_required
def redirect_to_school(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if secretariat_authenticate(request, conference) and request.method == 'POST':
        form = SchoolNameForm(request.POST)
        if form.is_valid():
            school = get_object_or_404(School, name=form.cleaned_data['name'])
            return HttpResponseRedirect(reverse(school_admin,
                                             args=(conference.url_name,school.url_name)))

    raise Http404

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
            
            return HttpResponseRedirect(reverse(conference_created, 
                                                args=(new_conference.url_name,)))
    else:
        conference_form = ConferenceForm()
        user_form = SecretariatUserForm()

    return render_response(request, 'conference/create-conference.html', {
        'conference_form': conference_form, 'secretariat_form' : user_form
    })

def conference_created(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    return render_response(request, 'conference/conference-created.html', {'conference' : conference,})
    