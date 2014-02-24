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
            ($rootScope, $location, $route, $http)->
                $http.defaults.headers.common.Authorization = "Token 8bbd840c67f4b7c233bea04fc9a48916e8b088d5"
                
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
            '$httpProvider'
            ($interpolateProvider, $routeProvider, $locationProvider, $httpProvider)->
                # Intercepts HTTP request to add cache for anonymous user
                # and to set the right csrf token from the cookies
                $httpProvider.interceptors.push('HttpInterceptor');
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                $locationProvider.html5Mode true

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
                    .when '/results/:id/embedded',
                            controller: 'ResultsCtrl'
                            templateUrl: '/partial/results.embedded.html'
                    .when '/about',
                        templateUrl: '/partial/about.html'
    ])