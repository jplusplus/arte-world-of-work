# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-26 22:28:38
# Last Modified time: 2014-04-10 12:10:34
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

class PageCtrl
    @$inject: ['$scope', '$location', '$translate', '$cookies']

    constructor: (@scope, @location, @$translate, @cookies)->
        @title = ''

        @scope.Page = this        
        @scope.currentLang = @currentLang
        
        if @cookies.django_language
            @langChanged(@cookies.django_language)

    langChanged: (lang)=>
        return unless lang
        @$translate.use(lang)
        @cookies.django_language = lang

    currentLang: (lang)=>
        if lang?
            @langChanged(lang)
        @$translate.use()

    title: (title) =>
        if title?
            @title = title
        @title 

angular.module('arte-ww').controller 'PageCtrl', PageCtrl
