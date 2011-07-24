from django.contrib.auth import REDIRECT_FIELD_NAME, login, views
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, \
    HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from recaptcha.client import captcha
from regimun_app.forms import DetailedUserCreationForm
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
        
        if settings.DEBUG:
            print errordata
        
        raise ValueError("AJAX error:\n" + errordata);
    raise Http404
