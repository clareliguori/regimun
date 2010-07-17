from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^registration/', include('django_regimun.regimun_app.urls')),
    (r'^admin/', include(admin.site.urls)),

)
