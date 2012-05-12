from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

admin.autodiscover()

# simple redirection to events - remove it (and the first url pattern)
# if you want to have a different view under the base URL.
def redirect_to_events(request):
    return redirect('home')

urlpatterns = patterns('',
    url(r'^$', redirect_to_events, {}, 'redirect-to-events'),                   
    url(r'^events/', include('events.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'events.views.login_user', {}, 'login-redirect'),
)

urlpatterns += staticfiles_urlpatterns()