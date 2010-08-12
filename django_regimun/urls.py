from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    (r'^registration/', include('regimun_app.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'regimun_app/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'regimun_app/logout.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )