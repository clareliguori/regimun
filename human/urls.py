from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin, auth
admin.autodiscover()

from regimun_app.views.general import register_user

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

#    (r'^PIE.htc', pie_with_headers, {}),

    # account management
    url(r'^accounts/login/$', auth.views.login,
        {'template_name': 'accounts/login.html',
        'redirect_field_name' : 'next'}),

    url(r'^accounts/logout/$', auth.views.logout_then_login, {}),

    url(r'^accounts/change_password/$', auth.views.password_change,
        {'template_name': 'accounts/password_change_form.html',
        'post_change_redirect' : '../password_changed/'}),

    url(r'^accounts/password_changed/$', auth.views.password_change_done,
        {'template_name': 'accounts/password_change_done.html'}),

    url(r'^accounts/request_password_reset/$', auth.views.password_reset, {
        'template_name': 'accounts/password_reset_form.html',
        'email_template_name' : 'accounts/password_reset_email.html',
        'post_reset_redirect' : '../password_reset_requested/'}),

    url(r'^accounts/password_reset_requested/$',
        auth.views.password_reset_done, {
            'template_name': 'accounts/password_reset_done.html'}),

    url(r'^accounts/password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth.views.password_reset_confirm, {
            'template_name': 'accounts/password_reset_confirm.html',
            'post_reset_redirect' : '../password_reset_complete/'}),

    url(r'^accounts/password_reset/password_reset_complete/$',
        auth.views.password_reset_complete, {
            'template_name': 'accounts/password_reset_complete.html'}),

    url(r'^accounts/register/$', register_user, {'redirect_field_name' : 'next'}),

    url(r'', include('regimun_app.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
