from django.conf.urls.defaults import patterns
from django.views.generic.list_detail import object_detail, object_list
from regimun_app.ajax.school import school_ajax_functions
from regimun_app.ajax.secretariat import conference_ajax_functions
from regimun_app.views.general import upload_progress
from regimun_app.views.school_admin import *
from regimun_app.views.secretariat_admin import *

conferences = Conference.objects.all()

@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

urlpatterns = patterns('',
    # conferences index
    (r'^$', object_list, dict(queryset=conferences,template_name='conference_list.html')),
    
    # register new cconference
    (r'^new-conference/$', create_conference),

     # upload progress
    (r'^upload-progress/$', upload_progress),

   # conference was created
   # (r'^(?P<conference_slug>[-\w]+)/created$', conference_created),
    
    # schools index
    (r'^(?P<slug>[-\w]+)/$', object_detail, dict(queryset=conferences, slug_field='url_name', template_name='conference_detail.html')),

    # secretariat ajax calls
    (r'^(?P<conference_slug>[-\w]+)/secretariat/ajax/(?P<func_name>[-\w]+)$', conference_ajax_functions),
    
    # secretariat admin page
    (r'^(?P<slug>[-\w]+)/secretariat/$',
        limited_object_detail,
        dict(queryset=conferences, slug_field='url_name', template_name='secretariat/index.html')),

    # secretariat admin page - downloads
    (r'^(?P<conference_slug>[-\w]+)/secretariat/downloads/', spreadsheet_downloads),

    # invoices
    (r'^(?P<conference_slug>[-\w]+)/secretariat/invoices$', generate_all_invoices),

    # redirect to school page
    (r'^(?P<conference_slug>[-\w]+)/secretariat/see-school$', redirect_to_school),

    # register new school
    (r'^(?P<conference_slug>[-\w]+)/new-school/$', create_school),

    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/grant-school-access$', grant_school_access),

    # school page - downloads
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/downloads/', school_spreadsheet_downloads),
    
    # school invoice
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/invoice$', generate_invoice),
    
    # school ajax calls
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/ajax/(?P<func_name>[-\w]+)$', school_ajax_functions),

    # school admin page
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', school_admin),
)
