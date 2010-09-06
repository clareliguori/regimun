from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 
from recaptcha.client import captcha

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
