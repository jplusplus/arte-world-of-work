angular.module('arte-ww.filters', [])
angular.module('arte-ww.services', [])

arteww = angular
    .module('arte-ww', [
        'arte-ww.services',
        'arte-ww.filters',
        'pascalprecht.translate',
        'ui.bootstrap',
        'ngRoute',
        'ngResource'
    ])
    .run([
            '$rootScope'
            '$location'
            '$route'
            ($rootScope, $location, $route)->
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
            ($interpolateProvider, $routeProvider, $locationProvider)->
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                $locationProvider.html5Mode true
                # Bind routes to the controllers
                $routeProvider
                    .when('/', redirectTo: '/survey')
                    .when '/survey/:thematic_id',
                            controller: 'SurveyCtrl'
                            templateUrl: '/partial/survey.html'
                            category: 'survey'
                    .when '/results',
                            category: 'results'
                            controller: 'ResultsCtrl'
                            templateUrl: '/partial/results.html'
                    .when '/about',
                        templateUrl: '/partial/about.html'
    ])