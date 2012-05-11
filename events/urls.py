from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', home, {}, 'home'),
    url(r'^(?P<event_id>[0-9]+)/$', event, {}, 'event'),
    url(r'^url/(?P<secret_url>\w+)/$', event, {}, 'event-secret'),
    url(r'^search/$', search, {}, 'search'),
    url(r'^create/$', create_event, {}, 'create-event'),
    url(r'^create/ticket/$', create_ticket, {}, 'create-ticket'),
    # AUTH
    url(r'^login/$', login_user, {}, 'login'),
    url(r'^signup/$', register_user, {}, 'register'),
    url(r'^logout/$', logout_user, {}, 'logout'),
)

