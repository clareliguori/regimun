from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail
from regimun_app.models import Conference

conferences = Conference.objects.all()

@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

urlpatterns = patterns('',   #'django_regimun.regimun_app.views',
    # conferences index
    (r'^$', 'django.views.generic.list_detail.object_list', dict(queryset=conferences)),
    
    # check school and username availability
    #(r'^check_schoolname/', 'django_regimun.regimun_app.views.check_schoolname'),
    #(r'^check_username/', 'django_regimun.regimun_app.views.check_username'),

    # schools index
    (r'^(?P<slug>[-\w]+)/$',
        'django.views.generic.list_detail.object_detail',
        dict(queryset=conferences, slug_field='url_name')),

    # secretariat admin page
    (r'^(?P<slug>[-\w]+)/secretariat/$',
        limited_object_detail,
        dict(queryset=conferences, slug_field='url_name', template_name='regimun_app/secretariat/index.html')),

    # register new school
    (r'^(?P<conference_slug>[-\w]+)/new-school/$',
        'django_regimun.regimun_app.views.create_school'),

    # school was created
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/created$', 'django_regimun.regimun_app.views.school_created'),
    
    # school admin page
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', 'django_regimun.regimun_app.views.school_admin'),

)
