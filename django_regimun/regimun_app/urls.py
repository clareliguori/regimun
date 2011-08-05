from django.conf.urls.defaults import patterns
from django.views.generic.list_detail import object_detail, object_list
from regimun_app.ajax.school import school_ajax_functions
from regimun_app.ajax.secretariat import conference_ajax_functions
from regimun_app.views.general import upload_progress, ajax_error
from regimun_app.views.school_admin import *
from regimun_app.views.secretariat_admin import *

conferences = Conference.objects.all()

@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

urlpatterns = patterns('',
    # conferences index
    (r'^$', object_list, dict(queryset=conferences,template_name='conference_list.html')),
    
    # ajax error notification
    (r'^ajax-error/$', ajax_error),
    
    # register new conference
    (r'^new-conference/$', create_conference),

     # upload progress
    (r'^upload-progress/$', upload_progress),

   # conference was created
   # (r'^(?P<conference_slug>[-\w]+)/created$', conference_created),
    
    # conference index
    (r'^(?P<slug>[-\w]+)/$', object_detail, dict(queryset=conferences, slug_field='url_name', template_name='conference_detail.html')),

    # school index
    (r'^school/(?P<slug>[-\w]+)/$', school_index),

    # secretariat ajax calls
    (r'^(?P<conference_slug>[-\w]+)/secretariat/ajax/(?P<func_name>[-\w]+)$', conference_ajax_functions),
    
    # secretariat admin page
    (r'^(?P<slug>[-\w]+)/secretariat/$',
        limited_object_detail,
        dict(queryset=conferences, slug_field='url_name', template_name='secretariat/index.html')),

    # secretariat admin page - downloads
    (r'^(?P<conference_slug>[-\w]+)/secretariat/downloads/', spreadsheet_downloads),

    # invoices
    (r'^(?P<conference_slug>[-\w]+)/secretariat/invoices$', generate_all_invoices_pdf),
    (r'^(?P<conference_slug>[-\w]+)/secretariat/invoices-doc$', generate_all_invoices_doc),
    
    # redirect to school page
    (r'^(?P<conference_slug>[-\w]+)/secretariat/see-school$', redirect_to_school),

    # register new school
    (r'^(?P<conference_slug>[-\w]+)/new-school/$', register_school),

    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/grant-school-access$', grant_school_access),
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/add-me$', add_to_conference),

    # school page - downloads
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/downloads/', school_spreadsheet_downloads),
    
    # school invoice
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/invoice$', generate_invoice_pdf),
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/invoice-doc$', generate_invoice_doc),

    # school invoice - based on delegate requests
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/invoice-from-request$', generate_request_based_invoice),
   
    # school fees
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/fees$', get_fees_table),
   
    # school ajax calls
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/ajax/(?P<func_name>[-\w]+)$', school_ajax_functions),

    # school admin page
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', school_admin),
)
