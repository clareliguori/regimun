from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count, Sum
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from regimun_app.forms import ConferenceForm, SecretariatUserForm, \
    SchoolNameForm
from regimun_app.models import Conference, FacultySponsor, Delegate, Country, \
    Committee, Secretariat, School, FeeStructure, DelegatePosition, \
    CountryPreference, DelegateCountPreference, DelegationRequest, Payment
from regimun_app.utils import fetch_resources, UnicodeCSVWriter, \
    UnicodeCSVReader
from regimun_app.views.general import render_response, convert_html_to_doc
from regimun_app.views.school_admin import school_admin, \
    get_fees_table_from_data
from settings import MEDIA_ROOT
from xhtml2pdf import pisa
import csv

def staff_authenticate(request):
    return request.user.is_staff

def secretariat_authenticate(request, conference):
    if request.user.is_staff:
        return True

    try:
        request.user.secretariat_member.conferences.get(id=conference.id)
    except ObjectDoesNotExist:
        return False
    
    return True

@login_required
def spreadsheet_downloads(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if secretariat_authenticate(request, conference):
        response = HttpResponse(mimetype='text/csv')
        writer = UnicodeCSVWriter(response)
        
        if 'sponsor-contacts' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=sponsor-contacts-' + conference_slug + ".csv"            
            writer.writerow(['School', 'First Name', 'Last Name', 'E-mail Address', 'Phone',
                            'Street Address','Address 2','City','State / Province / Region','ZIP / Postal Code','Country'])
            
            sponsors = FacultySponsor.objects.select_related().filter(conferences__url_name__exact=conference_slug)
            
            for sponsor in sponsors:
                school = sponsor.school
                writer.writerow([school.name,
                                 sponsor.user.first_name, sponsor.user.last_name, sponsor.user.email, sponsor.phone,
                                 school.address_line_1, school.address_line_2, school.city, school.state, school.zip, school.address_country])
             
        elif 'delegates' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=delegates-' + conference_slug + ".csv" 
            writer.writerow(['School', 'Country', 'Committee', 'Title', 'First Name', 'Last Name'])
            
            delegates = Delegate.objects.select_related('position_assignment',\
                                                        'position_assignment__country',\
                                                        'position_assignment__school',\
                                                        'position_assignment__committee').filter(position_assignment__country__conference__url_name__exact=conference_slug)
            
            for delegate in delegates:
                writer.writerow([delegate.position_assignment.school.name, delegate.position_assignment.country.name,
                                 delegate.position_assignment.committee.name, delegate.position_assignment.title, 
                                 delegate.first_name, delegate.last_name])
            
        elif 'school-country-assignments' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=school-country-assignments-' + conference_slug + ".csv" 
            writer.writerow(['Country', 'School'])
            
            countries = Country.objects.filter(conference=conference)
            assignments = DelegatePosition.objects.filter(country__in=countries).values('school__name','country__name','country__pk')
            
            assignment_dict = dict()
            for item in assignments:
                if item['school__name'] != None:
                    assignment_dict.setdefault((item['country__name'],item['country__pk']), set()).add(item['school__name'])
                else:
                    assignment_dict.setdefault((item['country__name'],item['country__pk']), set())
            
            for country in countries:
                key = (country.name, country.pk)
                if assignment_dict.has_key(key):
                    writer.writerow([country.name, ','.join(assignment_dict[key])])            
            
        elif 'country-committee-assignments' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=country-committee-assignments-' + conference_slug + ".csv"             
            committees = Committee.objects.filter(conference=conference)
            countries = Country.objects.filter(conference=conference)
            
            headers = ['Country']
            for committee in committees:
                headers.append(committee.name)
            writer.writerow(headers)
            
            counts = DelegatePosition.objects.values('committee','country').annotate(count=Count('id'))
            
            count_dict = dict()
            for item in counts:
                count_dict[(item['country'],item['committee'])] = item['count']
            
            for country in countries:
                row = [country.name]
                for committee in committees:
                    row.append(str(count_dict.get((country.pk, committee.pk), 0)))
                writer.writerow(row)
        elif 'country-preferences' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=country-preferences-' + conference_slug + ".csv"             
            preferences = CountryPreference.objects.select_related().filter(request__conference=conference).order_by('request__school__name','last_modified')
    
            writer.writerow(['School','Rank','Country','Time Submitted'])
            
            current_school = ""
            rank = 1
            for preference in preferences:
                if preference.request.school.name == current_school:
                    rank = rank + 1
                else:
                    current_school = preference.request.school.name
                    rank = 1
                
                writer.writerow([current_school, str(rank), preference.country.name, preference.last_modified.strftime("%A, %d. %B %Y %I:%M%p")])                
        elif 'delegate-count-requests' in request.GET:
            response['Content-Disposition'] = 'attachment; filename=delegate-count-requests-' + conference_slug + ".csv"             
            preferences = DelegateCountPreference.objects.select_related().filter(request__conference=conference).order_by('request__school__name','request__created')
    
            writer.writerow(['School','Total Delegates Requested','Time Submitted'])
            
            for preference in preferences:
                writer.writerow([preference.request.school.name, preference.delegate_count, preference.request.created.strftime("%A, %d. %B %Y %I:%M%p")])                

        else:
            raise Http404
    else:
        raise Http404
    return response

@login_required
def generate_all_invoices_html(request, conference_slug, template, format):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    
    if secretariat_authenticate(request, conference):
        schools = School.objects.filter(conferences__id__exact=conference.id)
        feestructure = conference.feestructure
        
        delegate_counts = dict((k['position_assignment__school'],k['count']) for k in \
                                    Delegate.objects.filter(position_assignment__school__in=schools,position_assignment__country__conference=conference).values('position_assignment__school').annotate(count=Count('id')))
        
        country_school_pairs = DelegatePosition.objects.filter(school__in=schools, country__conference=conference, delegate__isnull=False).values('school','country').annotate(count=Count('id'))
        delegations_counts = dict()
        for pair in country_school_pairs:
            school_id = pair['school']
            delegations_counts[school_id] = delegations_counts.get(school_id, 0) + 1
         
        sponsor_counts = dict((k['school'],k['count']) for k in \
                                 FacultySponsor.objects.filter(school__in=schools,conferences__id__exact=conference.id).values('school').annotate(count=Count('id')))
        
        sums = dict((k['school'],float(k['sum'])) for k in \
                    Payment.objects.filter(school__in=schools,conference=conference).values('school').annotate(sum=Sum('amount')))
        
        schools_output = []

        for school in schools:
            school_context_dict = {
                'format' : format,
                'pagesize' : 'letter',
                'conference' : conference,
                'school' : school, 
                'fees_table' : get_fees_table_from_data(school, \
                                                        conference, \
                                                        feestructure, \
                                                        delegate_counts.setdefault(school.id, 0), \
                                                        delegations_counts.setdefault(school.id, 0), \
                                                        sponsor_counts.setdefault(school.id, 0), \
                                                        sums.setdefault(school.id, 0))}
            schools_output.append(render_to_string('invoice/invoice-body.html', school_context_dict, context_instance=RequestContext(request)))
        
        context_dict = {
            'format' : format,
            'pagesize' : 'letter',
            'conference' : conference,
            'school_invoices' : schools_output
        }
        return render_to_string(template, context_dict, context_instance=RequestContext(request))
    else:
        raise Http404

@login_required
def generate_all_invoices_pdf(request, conference_slug):
    response = http.HttpResponse()
    response['Content-Type'] ='application/pdf'
    response['Content-Disposition'] = 'attachment; filename=invoices-' + conference_slug + '.pdf'
    
    html = generate_all_invoices_html(request, conference_slug, 'invoice/all-invoices.html','pdf')
    pdf = pisa.CreatePDF(src=html, dest=response, show_error_as_pdf=True, link_callback=fetch_resources)
    if not pdf.err:
        return response
    else:
        raise ValueError("Error creating invoice PDF: " + pdf.err)

@login_required
def generate_all_invoices_doc(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    filename = 'invoices-' + conference_slug
    html = generate_all_invoices_html(request, conference_slug, 'invoice/all-invoices-doc.html','doc')
    return convert_html_to_doc(html, filename, conference)

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

@login_required
def create_conference(request):
    if request.method == 'POST' and staff_authenticate(request): 
        conference_form = ConferenceForm(request.POST)
        user_form = SecretariatUserForm(request.POST)
        
        if conference_form.is_valid() and user_form.is_valid():
            new_conference = conference_form.save(commit=False)
            new_conference.url_name = slugify(conference_form.cleaned_data['name'])
            new_conference.no_refunds_start_date = new_conference.start_date
            new_conference.save()
            
            # create default countries
            defaultCountriesList = MEDIA_ROOT + "default_countries.csv"
            countriesListReader = UnicodeCSVReader(open(defaultCountriesList))
            for row in countriesListReader:
                new_country = Country()
                new_country.conference = new_conference
                new_country.name = row[0].strip()
                new_country.url_name = slugify(new_country.name)
                new_country.country_code = row[1].strip()
                new_country.save()
                
            # create default committees and delegate positions
            defaultCommitteesList = MEDIA_ROOT + "default_committees.csv"
            committeesListReader = UnicodeCSVReader(open(defaultCommitteesList))
            for row in committeesListReader:
                new_committee = Committee()
                new_committee.conference = new_conference
                new_committee.name = row[0].strip()
                new_committee.url_name = slugify(new_committee.name)
                new_committee.save()
            
            # default fee structure (free conference)
            feeStructure = FeeStructure()
            feeStructure.conference = new_conference
            feeStructure.save()
            
            user = user_form.save(commit=False)
            user.email = new_conference.email_address
            user.save()
            secretariat_user = Secretariat()
            secretariat_user.user = user
            secretariat_user.save()
            secretariat_user.conferences.add(new_conference)
            
            return HttpResponseRedirect('/' + new_conference.url_name + '/secretariat/')
    else:
        conference_form = ConferenceForm()
        user_form = SecretariatUserForm()

    return render_response(request, 'conference/create-conference.html', {
        'conference_form': conference_form, 'secretariat_form' : user_form
    })
    