
arteww = angular
    .module('arte-ww', [
        'arte-ww.services',
        'arte-ww.filters',
        'pascalprecht.translate',
        'ui.bootstrap',
        'ngRoute',
    ])
    .run([
            '$rootScope'
            '$location'
            '$route'
            ($rootScope, $location, $route)->
                $rootScope.location = $location

                $rootScope.currentCategory = -> return $location.path().split('/')[1]
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
                    .when '/', redirectTo: '/survey'
                    .when '/survey',
                        controller: 'SurveyCtrl'
                        templateUrl: '/partial/survey.html'

    ])

angular.module('arte-ww.filters', [])
angular.module('arte-ww.services', [])
