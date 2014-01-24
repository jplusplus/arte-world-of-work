
arteww = angular
    .module('arte-ww', ['arte-ww.services', 'arte-ww.filters', 'ui.bootstrap', 'ngRoute'])
    .run([
            '$rootScope'
            '$location'
            ($rootScope, $location)->
                $rootScope.location = $location
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
                    .when('/',  
                        controller : 'HomeCtrl'
                        templateUrl: "/partial/home.html"
                    )
    ])

angular.module('arte-ww.filters', [])
angular.module('arte-ww.services', [])
