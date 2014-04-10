#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-26 19:00:01
# Last Modified time: 2014-04-10 13:01:51
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Front-end URLs
    url(r'^$',                                                               'app.views.home',              name='home'),
    url(r'^about/$',                                                         'app.views.home',              name='about'),
    url(r'^survey/$',                                                        'app.views.home',              name='survey'),
    url(r'^results/$',                                                       'app.views.home',              name='results'),
    url(r'^results/[0-9]+/embedded$',                                        'app.views.embedded',          name='embedded'),
    url(r'^404/$',                                                           'app.views.home',              name='404'),
    url(r'^partial/(?P<partial_name>([a-zA-Z0-9_\-/\.]+))\.html$',           'app.views.partial',           name='partial'),
    url(r'^partial/directives/(?P<partial_name>([a-zA-Z0-9_\-/]+))\.html$',  'app.views.directive_partial', name='directive_partial'),
    # API application URLs
    url(r'^api/',                                                 include('app.api.urls')),
    # Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    
)
# settings.LOCAL_SETTINGS are set to false when on heroku
if settings.DEBUG and settings.LOCAL_SETTINGS:
    urlpatterns += patterns('',
        (r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )