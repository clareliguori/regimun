from django.conf.urls.defaults import *
from regimun_app.models import Conference

conferences = Conference.objects.all()

urlpatterns = patterns('',   #'django_regimun.regimun_app.views',
    # conferences index
    (r'^$', 'django.views.generic.list_detail.object_list', dict(queryset=conferences)),
    
    # schools index
    (r'^(?P<slug>[-\w]+)/$',
        'django.views.generic.list_detail.object_detail',
        dict(queryset=conferences, slug_field='url_name')),

    # secretariat admin page
    (r'^(?P<slug>[-\w]+)/secretariat/$',
        'django.views.generic.list_detail.object_detail',
        dict(queryset=conferences, slug_field='url_name', template_name='regimun_app/secretariat/index.html')),

    # register new school
    (r'^(?P<slug>[-\w]+)/new-school/$',
        'django.views.generic.list_detail.object_detail',
        dict(queryset=conferences, slug_field='url_name', template_name='regimun_app/register-new-school.html')),
    
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', 'django_regimun.regimun_app.views.school_admin'),

)
