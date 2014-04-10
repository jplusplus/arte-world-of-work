#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 12:27:15
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

from django.conf.urls import patterns, include, url
from rest_framework import routers

from app.api import views


router = routers.DefaultRouter()

router.register(r'thematics',        views.ThematicViewSet)
router.register(r'questions',        views.QuestionViewSet,        base_name='question')
router.register(r'thematics-nested', views.NestedThematicViewSet,  base_name='thematic-nested')
router.register(r'thematics-result', views.ThematicResultsViewSet, base_name='thematic-results')
router.register(r'countries',        views.CountryViewSet,         base_name='country')
router.register(r'user',             views.UserViewSet,            base_name='user')
router.register(r'my-answers',       views.MyAnswerViewSet,        base_name='my-answers')
router.register(r'answers',          views.AnswerViewSet,          base_name='answer')

urlpatterns = patterns('',
    url(r'^my-position/',  views.MyPositionView.as_view(), name='my-position'),
    url(r'^gplus-count/',  views.GPlusCount.as_view(), name='gplus-count'),
    url(r'^verify-token/', 'app.api.views.verify_auth_token', name='verify-token'),
)
urlpatterns += router.urls


