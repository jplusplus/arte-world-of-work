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
        'nouislider'
    ])
    .run([
            '$rootScope'
            '$location'
            '$route'
            '$http'
            '$translate'
            ($rootScope, $location, $route, $http, $translate)->

                $rootScope.setLang = (lang)->
                    $translate.use lang

                $rootScope.location = $location
                $rootScope.currentCategory = ->
                    # get the current category thanks to current root
                    category = null
                    if $route.current
                        category = $route.current.category or null
                    return category
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
                $translateProvider.useStaticFilesLoader
                    prefix: STATIC_URL + 'locale/'
                    suffix: '.json'

                $translateProvider.preferredLanguage 'en' 
                # Bind routes to the controllers
                $routeProvider
                    .when('/', redirectTo: '/survey')
                    .when '/survey',
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
    ])