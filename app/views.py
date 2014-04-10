#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-04-07 17:49:13
# Last Modified time: 2014-04-10 13:01:37
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

from django.conf      import settings
from django.http      import Http404
from django.shortcuts import render_to_response, redirect
from django.template  import TemplateDoesNotExist, RequestContext

def home(request):
    # Render template without any argument
    response = render_to_response('home.dj.html', context_instance=RequestContext(request))            
    # Homepage always set a language cookie
    if request.COOKIES.get('django_language') is None:
        response.set_cookie('django_language', settings.LANGUAGE_CODE)
    return response

def embedded(request):
    # Render template without any argument
    response = render_to_response('embedded.dj.html', context_instance=RequestContext(request))
    return response

def directive_partial(request, partial_name=None):
    template_name = 'partials/directives/' + partial_name + '.dj.html'
    try:
        return render_to_response(template_name, context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404

def partial(request, partial_name=None):
    template_name = 'partials/' + partial_name + '.dj.html'
    try:
        return render_to_response(template_name, context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404

def not_found(request):
    return redirect("/404/")

