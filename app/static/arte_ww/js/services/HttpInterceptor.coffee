# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-24 12:40:40
# Last Modified time: 2014-04-10 12:12:05
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

isApi = (url) -> ((url.indexOf 'api') is 0) or (url.indexOf '/api') is 0

angular.module('arte-ww.services').factory('HttpInterceptor', [ '$q', '$cookies', ($q, $cookies)->
    request: (config)->
        config = config or $q.when(config)
        if $cookies.django_language
            config.headers = config.headers or {}
            config.headers['django_language'] = $cookies.django_language
        # Add CSRF Token for post request
        if $cookies.csrftoken?
            config.headers = config.headers or {}
            config.headers['X-CSRFToken'] = $cookies.csrftoken
        # Add API Token if needed
        if (isApi config.url) and $cookies.apitoken?
            config.headers = config.headers or {}
            config.headers['Authorization'] = "Token #{$cookies.apitoken}"
        # do something on success
        return config
])
