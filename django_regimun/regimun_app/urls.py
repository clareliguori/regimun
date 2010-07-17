from django.conf.urls.defaults import *

urlpatterns = patterns('django_regimun.regimun_app.views',

    (r'^$', 'conferences_index'),
    (r'^(?P<conference_slug>[-\w]+)/$', 'schools_index'),
    (r'^(?P<conference_slug>[-\w]+)/secretariat/$', 'conference_admin'),
    (r'^(?P<conference_slug>[-\w]+)/(?P<school_slug>[-\w]+)/$', 'school_admin'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
