from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.auth import views
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from regimun_app.views.general import register_user
import os

admin.autodiscover()

def pie_with_headers(request):
    filename = settings.MEDIA_ROOT + 'css/PIE.htc'
    wrapper = FileWrapper(open(filename))
    response = HttpResponse(wrapper, content_type='text/x-component')
    response['Content-Length'] = os.path.getsize(filename)
    return response

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^PIE.htc', pie_with_headers, {}),
    
    # account management
    (r'^accounts/login/$', views.login, {'template_name': 'accounts/login.html', 'redirect_field_name' : 'next'}),
    (r'^accounts/logout/$', views.logout_then_login, {}),
    (r'^accounts/change_password/$', views.password_change, {'template_name': 'accounts/password_change_form.html', 'post_change_redirect' : '../password_changed/'}),
    (r'^accounts/password_changed/$', views.password_change_done, {'template_name': 'accounts/password_change_done.html'}),
    (r'^accounts/request_password_reset/$', views.password_reset, {
                                                           'template_name': 'accounts/password_reset_form.html',
                                                           'email_template_name' : 'accounts/password_reset_email.html',
                                                           'post_reset_redirect' : '../password_reset_requested/'}),
    (r'^accounts/password_reset_requested/$', views.password_reset_done, {'template_name': 'accounts/password_reset_done.html'}),
    (r'^accounts/password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html', 'post_reset_redirect' : '../password_reset_complete/'}),
    (r'^accounts/password_reset_complete/$', views.password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}),
    (r'^accounts/register/$', register_user, {'redirect_field_name' : 'next'}),

    (r'^', include('regimun_app.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
