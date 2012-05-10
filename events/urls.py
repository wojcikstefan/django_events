from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', home, {}, 'home'),
    url(r'^(?P<event_id>[0-9]+)', event, {}, 'event'),
    url(r'^create/$', create_event, {}, 'create-event'),
    # AUTH
    url(r'^login/$', login_user, {}, 'login'),
    url(r'^signup/$', register_user, {}, 'register'),
    url(r'^logout/$', logout_user, {}, 'logout'),
)

