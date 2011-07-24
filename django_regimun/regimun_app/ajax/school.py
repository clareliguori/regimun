from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from regimun_app.forms import SchoolMailingAddressForm, EditFacultySponsorForm, \
    DelegateNameForm
from regimun_app.models import Conference, School, FacultySponsor, \
    DelegatePosition, Delegate, CountryPreference, Country, DelegateCountPreference, \
    DelegationRequest
from regimun_app.views.school_admin import school_authenticate
from datetime import datetime
import inspect
import smtplib
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
                #return HttpResponse("<html><body>" + return_value + "</body></html>")
            
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
    
def edit_delegate(request, school):
    if request.method == 'POST':
        position_pk = request.POST.get('position_pk','')
        delegate_position = DelegatePosition.objects.get(pk=position_pk)
        if delegate_position.school == school:
            try:
                delegate = Delegate.objects.get(position_assignment=delegate_position)
            except Delegate.DoesNotExist:
                delegate = Delegate()
                delegate.position_assignment = delegate_position
            form = DelegateNameForm(data=request.POST, instance=delegate)
            if form.is_valid():
                delegate = form.save(commit=False)
                delegate.save()
                return simplejson.dumps({'name':delegate.first_name + " " + delegate.last_name, 'position_pk':position_pk})
            else:
                return simplejson.dumps({'form':form.as_p(), 'position_pk':position_pk})

def get_edit_delegate_form(request, school):
    if request.method == 'POST':
        position_pk = request.POST.get('position_pk','')
        delegate_position = DelegatePosition.objects.get(pk=position_pk)
        if delegate_position.school == school:
            try:
                delegate = Delegate.objects.get(position_assignment=delegate_position)
                form = DelegateNameForm(instance=delegate)
            except Delegate.DoesNotExist:
                form = DelegateNameForm()
            return simplejson.dumps({'form':form.as_p(), 'position_pk':position_pk})

def remove_delegate(request, school):
    if request.method == 'POST':
        position_pk = request.POST.get('position_pk','')
        delegate_position = DelegatePosition.objects.get(pk=position_pk)
        if delegate_position.school == school:
            try:
                delegate = Delegate.objects.get(position_assignment=delegate_position)
                delegate.delete()
            except Delegate.DoesNotExist:
                pass
            return simplejson.dumps({'position_pk':position_pk})

def get_country_preferences(request, school):
    preferences = CountryPreference.objects.select_related('country').filter(request__school=school)
    current_preferences = []
    for preference in preferences:
        current_preferences.append(preference.country.pk)
    
    available_positions = DelegatePosition.objects.select_related('country').filter(school=None).order_by('country__name')
    available_countries = {}
    for position in available_positions:
        available_countries[position.country.pk] = position.country.name
    
    options = []
    for pk, name in available_countries.items():
        options.append("<option value=\"")
        options.append(str(pk))
        options.append("\">")
        options.append(name)
        options.append("</option>")
    
    delegate_count = 0
    try:
        delegate_count = DelegateCountPreference.objects.get(request__school=school).delegate_count
    except ObjectDoesNotExist:
        pass
    
    return simplejson.dumps({'preferences':current_preferences, 'delegate_count':delegate_count, 'available_countries':''.join(options)})

def set_country_preferences(request, school):
    if request.method == 'POST':
        try:
            delegation_request = DelegationRequest.objects.get(school=school)
        except ObjectDoesNotExist:
            delegation_request = DelegationRequest()
            delegation_request.school = school
            delegation_request.save()
        
        # remove current preferences
        CountryPreference.objects.filter(request=delegation_request).delete()
        DelegateCountPreference.objects.filter(request=delegation_request).delete()
        country_names = []
        count = 0
        country_index = 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M:")    # MySQL does not support microseconds, so we have to manually order the countries by seconds
        
        for pref_num, country_pk in request.POST.items():
            if pref_num == 'total_count':
                try:
                    count = int(country_pk)
                    count_pref = DelegateCountPreference()
                    count_pref.request = delegation_request
                    count_pref.delegate_count = count
                    count_pref.save()
                except TypeError:
                    pass  
            else:
                try:
                    country = Country.objects.get(pk=country_pk)
                except Country.DoesNotExist:
                    pass
                else:
                    if country.conference == school.conference:
                        # make sure this preference doesnt already exist
                        if country.name not in country_names:                        
                            pref = CountryPreference()
                            pref.country = country
                            pref.request = delegation_request
                            pref.last_modified = now + str(country_index)
                            pref.save()
                            country_index = country_index + 1
                            country_names.append(country.name)

        if len(country_names) > 0:
            # send notification email
            sender = school.conference.email_address
            to = school.conference.email_address
            
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Country Preferences Submission: " + school.name
            msg['From'] = sender
            msg['To'] = to
            
            # Body of the message (a plain-text and an HTML version).
            text = "Country preferences submitted for " + school.name + "\n"
            for i in range(len(country_names)):
                text += str(i+1) + ": " + country_names[i] + "\n"
            
            html = """\
            <html>
              <head></head>
              <body>
                <p>Country preferences submitted for <b>
            """
            html += school.name + "</b>:<ol>"
            for name in country_names:
                html += "<li>" + name + "</li>"
            
            html += "</ol>Total delegates requested: " + str(count) + "</p></body></html>"

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            
            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)
            
            # Send the message via local SMTP server.
            s = smtplib.SMTP('localhost')
            s.sendmail(sender, to, msg.as_string())
            s.quit()
        
        return simplejson.dumps({'success':True})
        