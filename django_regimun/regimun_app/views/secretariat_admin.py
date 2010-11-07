from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from ho import pisa
from regimun_app.forms import ConferenceForm, SecretariatUserForm, \
    SchoolNameForm
from regimun_app.models import Conference, FacultySponsor, Delegate, Country, \
    Committee, Secretariat, School, FeeStructure, DelegatePosition, \
    CountryPreference, DelegateCountPreference
from regimun_app.utils import fetch_resources
from regimun_app.views.general import render_response
from regimun_app.views.school_admin import school_admin
from settings import MEDIA_ROOT
import StringIO
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
            writer.writerow(['Country', 'School'])
            
            countries = Country.objects.filter(conference=conference)
            
            for country in countries:
                current_positions = DelegatePosition.objects.select_related().filter(country=country)
                if len(current_positions) > 0:
                    school = current_positions[0].school
                    if school:
                        writer.writerow([country.name, school.name])
                    else:
                        writer.writerow([country.name, " "])            

        elif 'country-committee-assignments' in request.GET:
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
        elif 'country-preferences' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=country-preferences-' + conference_slug + ".csv"             
            preferences = CountryPreference.objects.select_related().filter(school__conference=conference).order_by('school__name','last_modified')
    
            writer.writerow(['School','Rank','Country','Time Submitted'])
            
            current_school = ""
            rank = 1
            for preference in preferences:
                if preference.school.name == current_school:
                    rank = rank + 1
                else:
                    current_school = preference.school.name
                    rank = 1
                
                writer.writerow([current_school, str(rank), preference.country.name, preference.last_modified.strftime("%A, %d. %B %Y %I:%M%p")])                
        elif 'delegate-count-requests' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=delegate-count-requests-' + conference_slug + ".csv"             
            preferences = DelegateCountPreference.objects.select_related().filter(school__conference=conference).order_by('school__name','last_modified')
    
            writer.writerow(['School','Total Delegates Requested','Time Submitted'])
            
            for preference in preferences:
                writer.writerow([preference.school.name, preference.delegate_count, preference.last_modified.strftime("%A, %d. %B %Y %I:%M%p")])                

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
        
        schools = School.objects.select_related().filter(conference=conference)
        context_dict = {
            'pagesize' : 'letter',
            'conference' : conference,
            'schools' : schools, }
        html = render_to_string('secretariat/all-invoices.html', context_dict, context_instance=RequestContext(request))
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
        if not pdf.err:
            response = http.HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=invoices-' + conference_slug + '.pdf'
            return response
        else:
            raise Http404
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
            defaultCountriesList = MEDIA_ROOT + "default_countries.csv"
            countriesListReader = csv.reader(open(defaultCountriesList))
            for row in countriesListReader:
                new_country = Country()
                new_country.conference = new_conference
                new_country.name = row[0]
                new_country.url_name = slugify(new_country.name)
                new_country.country_code = row[1]
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
            
            # default fee structure (free conference)
            feeStructure = FeeStructure()
            feeStructure.conference = new_conference
            feeStructure.late_registration_start_date = new_conference.start_date
            feeStructure.save()
            
            user = user_form.save(commit=False)
            user.email = new_conference.email_address
            user.save()
            secretariat_user = Secretariat()
            secretariat_user.user = user
            secretariat_user.conference = new_conference
            secretariat_user.save()
            
            return HttpResponseRedirect('/' + new_conference.url_name + '/secretariat/')
    else:
        conference_form = ConferenceForm()
        user_form = SecretariatUserForm()

    return render_response(request, 'conference/create-conference.html', {
        'conference_form': conference_form, 'secretariat_form' : user_form
    })
    