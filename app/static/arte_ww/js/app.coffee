# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-04-07 17:43:14
# Last Modified time: 2014-04-10 12:27:05
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth perception of world of work
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

angular.module('arte-ww.services', ['ngCookies'])
angular.module('arte-ww.filters',  [])
angular.module('arte-ww.utils',    [])

arteww = angular
    .module('arte-ww', [
        'arte-ww.utils',
        'arte-ww.services',
        'arte-ww.filters',
        'pascalprecht.translate',
        'ui.bootstrap',
        'ngCookies',
        'ngRoute',
        'ngResource',
        'ngAnimate',
        'nouislider',
        'ngSanitize'
    ])
    .run([
        '$rootScope'
        '$location'
        '$route'
        '$translate'
        '$cookies'
        'UserPosition'
        ($rootScope, $location, $route, $translate, $cookies, UserPosition)->
            search_params = $location.search()
            # Activate arte mode
            $rootScope.shouldDisplayArte = search_params.arte                     
            # Update the current language
            $cookies.django_language = search_params.lang or $cookies.django_language
            $translate.use $cookies.django_language

            $rootScope.location = $location
            $rootScope.currentCategory = ->
                # get the current category thanks to current root
                category = null
                if $route.current
                    category = $route.current.category or null
                return category

            $rootScope.backToBeginning = ->
                UserPosition.thematicPosition 0
                UserPosition.elementPosition 0
                $location.url "/"

            $rootScope.safeApply = (fn)->
                phase = @$root.$$phase
                if phase is "$apply" or phase is "$digest"
                    do fn if fn and (typeof (fn) is "function")
                else
                    @$apply fn
    ])
    # Second run where dependancies need the previous call to be ended
    .run([
        "$rootScope",
        "Xiti",
        "ThirdParty"
        ($rootScope, Xiti, ThirdParty)->
            # Xiti service must be available everywhere             
            $rootScope.xiti = Xiti

            # Get thirdParty helpers
            $rootScope.thirdParty = ThirdParty
    ])
    .config([
            '$interpolateProvider'
            '$routeProvider'
            '$locationProvider'
            '$translateProvider'
            '$httpProvider'
            '$sceDelegateProvider'
            ($interpolateProvider, $routeProvider, $locationProvider, $translateProvider, $httpProvider, $sceDelegateProvider)->
                $sceDelegateProvider.resourceUrlWhitelist ['self', 'http://vine.co', 'https://vine.co']
                # Intercepts HTTP request to add cache for anonymous user
                # and to set the right csrf token from the cookies
                $httpProvider.interceptors.push 'HttpInterceptor'
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                # such html5 mode.
                $locationProvider.html5Mode true
                # translation configuration 
                STATIC_URL = window.STATIC_URL or "http://localhost:9876/static/"
                $translateProvider.useStaticFilesLoader
                    prefix: STATIC_URL + 'arte_ww/locale/'
                    suffix: '.json'

                $translateProvider.preferredLanguage 'en' 
                # Bind routes to the controllers
                $routeProvider
                    .when('/', redirectTo: '/survey')
                    .when '/survey',
                            reloadOnSearch: no
                            controller: 'SurveyCtrl'
                            templateUrl: '/partial/survey.html'
                            category: 'survey'
                    .when '/results',
                            category: 'results'
                            controller: 'ResultsCtrl'
                            templateUrl: '/partial/results.html'
                            reloadOnSearch: no
                    .when '/results/:id/embedded',
                            controller: 'ResultsCtrl'
                            templateUrl: '/partial/results.embedded.html'
                    .when '/about',
                        templateUrl: '/partial/about.html'
                        reloadOnSearch: no
    ])