from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify, date
from django.template.loader import render_to_string
from regimun_app.forms import NewSchoolForm, NewFacultySponsorForm
from regimun_app.models import Conference, School, FacultySponsor, Committee, \
    DelegatePosition, Country, CountryPreference, DelegateCountPreference
from regimun_app.templatetags.currencyformat import currencyformat
from regimun_app.utils import fetch_resources
from regimun_app.views.general import render_response, get_recaptcha_response, \
    convert_html_to_doc
from xhtml2pdf import pisa
import csv
import re
import settings

def school_authenticate(request, conference, school):
    if not is_school_registered(conference, school):
        return False
    
    if request.user.is_staff:
        return True
    
    try:
        secretariat_member = request.user.secretariat_member
        try:
            secretariat_member.conferences.get(id=conference.id)
        except Conference.DoesNotExist:
            return False
    except ObjectDoesNotExist:
        pass
    
    try:
        return request.user.faculty_sponsor.school.pk == school.pk
    except ObjectDoesNotExist:
        return False

def is_school_registered(conference, school):
    try:
        school.conferences.get(id=conference.id)
    except Conference.DoesNotExist:
        return False
    return True 

@login_required
def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)    
    school = get_object_or_404(School, url_name=school_slug)
    feestructure = conference.feestructure
    sponsors = FacultySponsor.objects.filter(school=school,conferences__id__exact=conference.id)
    fees_table = get_fees_table_from_data(school, \
                                          conference, \
                                          feestructure, \
                                          school.facultysponsor_set.filter(conferences__id__exact=conference.id).count(), \
                                          school.get_filled_delegate_positions_count(conference), \
                                          school.get_delegations_count(conference), \
                                          school.get_late_delegate_registrations_count(feestructure.late_delegate_registration_start_date,conference), \
                                          school.get_delegate_request_date(conference), \
                                          school.total_payments(conference))
    country_preferences = get_country_preferences_html(school,conference)
    return render_response(request, 'school/index.html', {'conference' : conference, 
                                                          'school' : school, 
                                                          'fees_table' : fees_table,
                                                          'country_preferences' : country_preferences,
                                                          'sponsors' : sponsors})

def create_school(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    if request.method == 'POST': 
        school_form = NewSchoolForm(request.POST)
        sponsor_form = NewFacultySponsorForm(request.POST)
        captcha_response = get_recaptcha_response(request)
        
        if school_form.is_valid():
            if request.user.is_authenticated() or sponsor_form.is_valid():
                if captcha_response.is_valid:
                    new_school = School()
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
                    new_school.conferences.add(conference)
                    
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
                    new_sponsor.conferences.add(conference)
       
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
            sponsor.conferences.add(conference)

            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            return HttpResponseRedirect(redirect_to)

    return render_response(request, "school/wrong-access-code.html", {'conference' : conference, 'school' : school})

@login_required
def generate_invoice_html(request, conference_slug, school_slug, template):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    feestructure = conference.feestructure
    
    if school_authenticate(request, conference, school):
        context_dict = {
        'pagesize' : 'letter',
        'conference' : conference,
        'school' : school, 
        'fees_table' : get_fees_table_from_data(school, \
                                          conference, \
                                          feestructure, \
                                          school.facultysponsor_set.filter(conferences__id__exact=conference.id).count(), \
                                          school.get_filled_delegate_positions_count(conference), \
                                          school.get_delegations_count(conference), \
                                          school.get_late_delegate_registrations_count(feestructure.late_delegate_registration_start_date,conference), \
                                          school.get_delegate_request_date(conference), \
                                          school.total_payments(conference))}
        return render_to_string(template, context_dict, context_instance=RequestContext(request))
    else:
        raise Http404

@login_required
def generate_invoice_pdf(request, conference_slug, school_slug):
    response = http.HttpResponse()
    response['Content-Type'] ='application/pdf'
    response['Content-Disposition'] = 'attachment; filename=invoice-' + conference_slug + "-" + school_slug + '.pdf'
    
    html = generate_invoice_html(request, conference_slug, school_slug, 'invoice/invoice.html')
    pdf = pisa.CreatePDF(src=html, dest=response, show_error_as_pdf=True, link_callback=fetch_resources)
    if not pdf.err:
        return response
    else:
        raise ValueError("Error creating invoice PDF: " + pdf.err)

@login_required
def generate_invoice_doc(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    filename = 'invoice-' + conference_slug + "-" + school_slug
    html = generate_invoice_html(request, conference_slug, school_slug, 'invoice/invoice-doc.html')
    return convert_html_to_doc(html, filename, conference)

@login_required
def generate_request_based_invoice(request, conference_slug, school_slug):
    response = http.HttpResponse()
    response['Content-Type'] ='application/pdf'
    response['Content-Disposition'] = 'attachment; filename=invoice-' + conference_slug + "-" + school_slug + '.pdf'
    
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    feestructure = conference.feestructure
    
    if school_authenticate(request, conference, school):
        context_dict = {
        'pagesize' : 'letter',
        'conference' : conference,
        'school' : school, 
        'fees_table' : get_request_fees_table_from_data(school, \
                                          conference, \
                                          feestructure)}
        html = render_to_string('invoice/invoice-from-request.html', context_dict, context_instance=RequestContext(request))
        pdf = pisa.CreatePDF(src=html, dest=response, show_error_as_pdf=True, link_callback=fetch_resources)
        if not pdf.err:
            return response
        else:
            raise ValueError("Error creating invoice PDF: " + pdf.err)
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

            counts = DelegatePosition.objects.values('committee','country').annotate(count=Count('id'))
            
            count_dict = dict()
            for item in counts:
                count_dict[(item['country'],item['committee'])] = item['count']
            
            for country in countries:
                row = [country.name]
                for committee in committees:
                    row.append(str(count_dict.get((country.pk, committee.pk), 0)))
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
    feestructure = conference.feestructure
    
    if school_authenticate(request, conference, school):
        return HttpResponse(get_fees_table_from_data(school, \
                                          conference, \
                                          feestructure, \
                                          school.facultysponsor_set.filter(conferences__id__exact=conference.id).count(), \
                                          school.get_filled_delegate_positions_count(conference), \
                                          school.get_delegations_count(conference), \
                                          school.get_late_delegate_registrations_count(feestructure.late_delegate_registration_start_date,conference), \
                                          school.get_delegate_request_date(conference), \
                                          school.total_payments(conference)))
    raise Http404

def get_country_preferences_html(school,conference):
    
    country_preferences = []
    preferences = CountryPreference.objects.select_related('country').filter(request__school=school,request__conference=conference)
    if len(preferences) == 0:
        country_preferences.append("<i>No country preferences have been submitted.</i>")
    else:
        country_preferences.append("<ol>")
        for pref in preferences:
            country_preferences.append('<li>' + pref.country.name + "</li>")
        country_preferences.append("</ol>")
    
    delegate_count = 0
    try:
        delegate_count = DelegateCountPreference.objects.get(request__school=school,request__conference=conference).delegate_count
    except ObjectDoesNotExist:
        pass
    
    context_dict = {
        'school' : school,
        'country_preferences': ''.join(country_preferences),
        'delegate_count': delegate_count,
        }
    return render_to_string('school/country-preferences.html', context_dict)

def get_fees_table_from_data(school, conference, feestructure, sponsor_count, delegates_count, delegations_count, late_delegates_count, delegation_request_date, total_payments):
    output = []
    
    left_style = "style=\"padding: 3px; text-align: left\""
    right_style = "style=\"padding: 3px; text-align: right\""
    
    total_fee = 0.0

    output.append(fees_table_header())
            
    if feestructure.per_school != 0:
        per_school = str(currencyformat(feestructure.per_school))
        output.append("<tr>")
        output.append("<td " + left_style + ">School Fee</td>")
        output.append("<td " + right_style + ">" + per_school + "</td>")
        output.append("<td " + right_style + ">1</td>")
        output.append("<td " + right_style + ">" + per_school + "</td>")
        output.append("</tr>")
        total_fee += float(feestructure.per_school)
        
    if feestructure.per_country != 0:
        per_country_fee = float(delegations_count * feestructure.per_country)
        output.append("<tr>")
        output.append("<td " + left_style + ">Country Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_country)) + "</td>")
        output.append("<td " + right_style + ">" + str(delegations_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_country_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_country_fee
        
    if feestructure.per_delegate != 0:
        per_delegate_fee = float(delegates_count * feestructure.per_delegate)
        output.append("<tr>")
        output.append("<td " + left_style + ">Delegate Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_delegate)) + "</td>")
        output.append("<td " + right_style + ">" + str(delegates_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_delegate_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_delegate_fee

    if feestructure.per_sponsor != 0:
        per_sponsor_fee = float(sponsor_count * feestructure.per_sponsor)
        output.append("<tr>")
        output.append("<td " + left_style + ">Sponsor/Advisor Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_sponsor)) + "</td>")
        output.append("<td " + right_style + ">" + str(sponsor_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_sponsor_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_sponsor_fee
    
    if feestructure.per_school_late_fee > 0:
        if delegation_request_date != None and delegation_request_date.date() >= feestructure.late_registration_start_date:
            late_fee_str = str(currencyformat(feestructure.per_school_late_fee))
            output.append("<tr>")
            output.append("<td " + left_style + ">School Registration Late Fee</td>")
            output.append("<td " + right_style + ">" + late_fee_str + "</td>")
            output.append("<td " + right_style + ">1</td>")
            output.append("<td " + right_style + ">" + late_fee_str + "</td>")
            output.append("</tr>")
            total_fee += float(feestructure.per_school_late_fee)
    
    if feestructure.per_delegate_late_fee != 0 and late_delegates_count > 0:
            late_reg_fee = float(late_delegates_count * feestructure.per_delegate_late_fee)
            output.append("<tr>")
            output.append("<td " + left_style + ">Delegate Registration Late Fee</td>")
            output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_delegate_late_fee)) + "</td>")
            output.append("<td " + right_style + ">" + str(late_delegates_count) + "</td>")
            output.append("<td " + right_style + ">" + str(currencyformat(late_reg_fee)) + "</td>")
            output.append("</tr>")
            total_fee += late_reg_fee
    
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Total Fees</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_fee) + "</th></tr>")
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Paid</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_payments) + "</th></tr>")
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Balance Due</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_fee - total_payments) + "</th></tr>");
    
    output.append(fees_table_footer(conference, feestructure))
    
    return ''.join(output)
    
def get_request_fees_table_from_data(school, conference, feestructure):
    output = []
    
    left_style = "style=\"padding: 3px; text-align: left\""
    right_style = "style=\"padding: 3px; text-align: right\""
    
    total_fee = 0.0

    output.append(fees_table_header())
            
    if feestructure.per_school != 0:
        per_school = str(currencyformat(feestructure.per_school))
        output.append("<tr>")
        output.append("<td " + left_style + ">School Fee</td>")
        output.append("<td " + right_style + ">" + per_school + "</td>")
        output.append("<td " + right_style + ">1</td>")
        output.append("<td " + right_style + ">" + per_school + "</td>")
        output.append("</tr>")
        total_fee += float(feestructure.per_school)
        
    if feestructure.per_country != 0:
        delegations_count = school.get_assigned_countries_count(conference)
        per_country_fee = float(delegations_count * feestructure.per_country)
        output.append("<tr>")
        output.append("<td " + left_style + ">Country Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_country)) + "</td>")
        output.append("<td " + right_style + ">" + str(delegations_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_country_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_country_fee
        
    if feestructure.per_delegate != 0:
        delegates_count = school.get_delegate_request_count(conference)
        per_delegate_fee = float(delegates_count * feestructure.per_delegate)
        output.append("<tr>")
        output.append("<td " + left_style + ">Delegate Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_delegate)) + "</td>")
        output.append("<td " + right_style + ">" + str(delegates_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_delegate_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_delegate_fee

    if feestructure.per_sponsor != 0:
        sponsor_count = school.facultysponsor_set.filter(conferences__id__exact=conference.id).count()
        per_sponsor_fee = float(sponsor_count * feestructure.per_sponsor)
        output.append("<tr>")
        output.append("<td " + left_style + ">Sponsor/Advisor Fee</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(feestructure.per_sponsor)) + "</td>")
        output.append("<td " + right_style + ">" + str(sponsor_count) + "</td>")
        output.append("<td " + right_style + ">" + str(currencyformat(per_sponsor_fee)) + "</td>")
        output.append("</tr>")
        total_fee += per_sponsor_fee
    
    if feestructure.per_school_late_fee > 0:
        delegation_request_date = school.get_delegate_request_date(conference)
        if delegation_request_date != None and delegation_request_date.date() >= feestructure.late_registration_start_date:
            late_fee_str = str(currencyformat(feestructure.per_school_late_fee))
            output.append("<tr>")
            output.append("<td " + left_style + ">School Registration Late Fee</td>")
            output.append("<td " + right_style + ">" + late_fee_str + "</td>")
            output.append("<td " + right_style + ">1</td>")
            output.append("<td " + right_style + ">" + late_fee_str + "</td>")
            output.append("</tr>")
            total_fee += float(feestructure.per_school_late_fee)
    
    total_payments = school.total_payments(conference)
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Total Fees</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_fee) + "</th></tr>")
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Paid</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_payments) + "</th></tr>")
    output.append("<tr><th style=\"font-weight: bold; padding: 3px; text-align: right\" colspan=\"3\">Balance Due</th><th style=\"font-weight: bold; padding: 3px; text-align: right\">")
    output.append(currencyformat(total_fee - total_payments) + "</th></tr>");
    
    output.append(fees_table_footer(conference, feestructure))
    
    return ''.join(output)
    
def fees_table_header():    
    output = []
    output.append("<div id=\"fees-table\">")
    output.append("<h3 style=\"margin: 0; font-size: 100%;\" >Conference Fees:</h3>")
    output.append("<table style=\"width: 100%; border: 1px solid; margin:0px; padding:6px;\">")
    output.append("<tbody><tr>")
    output.append("<th style=\"font-weight: bold; padding: 3px; text-align: left\">Fee</th>")
    output.append("<th style=\"font-weight: bold; padding: 3px; text-align: right\">Rate</th>")
    output.append("<th style=\"font-weight: bold; padding: 3px; text-align: right\">Quantity</th>")
    output.append("<th style=\"font-weight: bold; padding: 3px; text-align: right\">Amount</th>")
    output.append("</tr>")

    return ''.join(output)

def fees_table_footer(conference, feestructure):
    output = []
    output.append("</tbody></table><br/><br/>")
    if feestructure.per_school_late_fee != 0:
        output.append("Country preferences are due on " + date(feestructure.late_registration_start_date,"F jS") + ", after which late fees will be applied.<br/>")

    if feestructure.per_delegate_late_fee != 0:
        output.append("Delegate registration is due on " + date(feestructure.late_delegate_registration_start_date,"F jS") + ", after which late fees will be applied.<br/>")
    
    output.append("No refunds will be issued past " + date(feestructure.no_refunds_start_date, "F jS")) 
    output.append(".<br/><br/>Please mail all payment to: <br/>")
    output.append("<span style=\"padding-left: 30pt;\">" + conference.address_line_1)
    if conference.address_line_2:
        output.append(", " + conference.address_line_2)
    output.append("<br/></span><span style=\"padding-left: 30pt;\">" + conference.city + ", " + conference.state)
    if conference.zip:
        output.append(", " + conference.zip)
    if conference.address_country:
        output.append(", " + conference.address_country)
    output.append("<br/></span>Checks should be made out to " + conference.organization_name + ".</div>")
    
    return ''.join(output)
