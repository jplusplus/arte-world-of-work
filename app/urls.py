#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte - WoW
# -----------------------------------------------------------------------------
# Author : 
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Jan-2014
# Last mod : 14-Jan-2014
# -----------------------------------------------------------------------------
from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Front-end URLs
    url(r'^$',                                                    'app.views.home', name='home'),
    url(r'^404/$',                                                'app.views.home', name='404'),
    url(r'^partial/(?P<partial_name>([a-zA-Z0-9_\-/]+))\.html$',  'app.views.partial', name='partial'),
    # API application URLs
    url(r'^api/',                                                 include('app.api.urls')),
    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        (r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

