from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', home, {}, 'home'),
    url(r'^login/$', login_user, {}, 'login'),
    url(r'^logout/$', logout_user, {}, 'logout'),
)

