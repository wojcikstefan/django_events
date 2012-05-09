from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', home, {}, 'dj-ev-home'),
)

