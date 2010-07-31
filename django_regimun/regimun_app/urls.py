from django.conf.urls.defaults import patterns
from django.views.generic.list_detail import object_detail, object_list
from regimun_app.views import *

conferences = Conference.objects.all()

@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

urlpatterns = patterns('',   #'django_regimun.regimun_app.views',
    # conferences index
    (r'^$', object_list, dict(queryset=conferences)),
    
    # register new cconference
    (r'^new-conference/$', create_conference),

    # school was created
    (r'^(?P<conference_slug>[-\w]+)/created$', conference_created),
    
    # check school and username availability
    #(r'^check_schoolname/', 'django_regimun.regimun_app.views.check_schoolname'),
    #(r'^check_username/', 'django_regimun.regimun_app.views.check_username'),

    # schools index
    (r'^(?P<slug>[-\w]+)/$', object_detail, dict(queryset=conferences, slug_field='url_name')),

    # secretariat admin page
    (r'^(?P<slug>[-\w]+)/secretariat/$',
        limited_object_detail,
        dict(queryset=conferences, slug_field='url_name', template_name='regimun_app/secretariat/index.html')),

    # secretariat admin page
    (r'^(?P<conference_slug>[-\w]+)/secretariat/downloads/', spreadsheet_downloads),

    # register new school
    (r'^(?P<conference_slug>[-\w]+)/new-school/$', create_school),

    # school was created
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/created$', school_created),
    
    # school admin page
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', school_admin),

)
