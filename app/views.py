#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


# Create your views here.
