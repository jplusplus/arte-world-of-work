# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 11:45:20
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

class ResultService
    @$inject: ['$http']

    constructor: (@$http) ->

    get: (params, cb) =>
        request =
            method : 'GET'
            url : "/api/questions/#{params.id}/results"
            params : params.filters
        (@$http request).success cb

    post: (params, cb) =>
        request =
            method: 'POST'
            url : '/api/answers/#{params.question.id}'
            data: params.value

(angular.module 'arte-ww.services').service 'Result', ResultService