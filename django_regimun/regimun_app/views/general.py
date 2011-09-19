from django import http
from django.contrib.auth import REDIRECT_FIELD_NAME, views
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, \
    HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from recaptcha.client import captcha
from regimun_app.forms import DetailedUserCreationForm
import base64
import mimetypes
import os
import re
import settings

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

def get_recaptcha_response(request):
    captcha_response = \
    captcha.submit(request.POST.get("recaptcha_challenge_field", None),
                   request.POST.get("recaptcha_response_field", None),
                   "6LeeursSAAAAAAsPzg0VPYpkfP9lbtXL9Bmeysh-",
                   request.META.get("REMOTE_ADDR", None))
        
    return captcha_response

def register_user(request, template_name='accounts/register.html',
          redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == 'POST':
        form = DetailedUserCreationForm(data=request.POST)
        if form.is_valid():
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL
            new_user = form.save()
            return HttpResponseRedirect(reverse(views.login))
    else:
        form = DetailedUserCreationForm()

    return render_response(request, template_name, {'form': form, redirect_field_name: redirect_to})

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def ajax_error(request):
    if request.method == 'POST':
        errordata = request.POST.get('errordata', '')        
        raise ValueError("AJAX error:\n" + errordata)
    raise Http404

def convert_html_to_doc(html, filename, conference):
    response = http.HttpResponse()
    response['Content-Type'] ='application/msword'
    response['Content-Disposition'] = 'filename=' + filename + '.doc'

    if conference.logo:
        image_filepath = "media/" + os.path.basename(conference.logo.url)
        html = html.replace(settings.MEDIA_URL + "/" + conference.logo.url, image_filepath)
    
    # pack the html and image into a MIME file 
    doc = MIMEMultipart('related')
    part1 = MIMEBase('text', 'html')
    part1.set_payload(base64.encodestring(html.encode("UTF-8")),"utf-8")
    part1.add_header("Content-Location", "file:///C:/" + filename + ".htm")
    part1.replace_header("Content-Transfer-Encoding", "base64")
    doc.attach(part1)

    if conference.logo:
        conference.logo.open("rb")
        image_str = conference.logo.read()
        conference.logo.close()
        mimetype = mimetypes.guess_type(conference.logo.url)[0].split('/')
    
        part2 = MIMEBase(mimetype[0], mimetype[1])
        part2.set_payload(base64.encodestring(image_str))
        part2.add_header("Content-Location", "file:///C:/" + image_filepath)
        part2.add_header("Content-Transfer-Encoding", "base64")
    
        doc.attach(part2)
    
    response.content = doc.as_string()
    return response
