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
            '$routeParams'
            ($rootScope, $location, $routeParams)->
                $rootScope.location = $location
                $rootScope.currentCategory = -> $routeParams.category
    ])
    .config([
            '$interpolateProvider'
            '$routeProvider'
            '$locationProvider'
            ($interpolateProvider, $routeProvider, $locationProvider)->
                # little trick to have a named parameter 
                categories = 
                    default: 'survey'
                    survey: 
                        controller: 'SurveyCtrl'
                        templateUrl: '/partial/survey.html'

                    results: 
                        controller: 'ResultsCtrl'
                        templateUrl: '/partial/results.html'

                getCategory = (name)->
                    unless _.has(categories, name)
                        category = categories[categories.default]
                    else
                        category = categories[name]
                    return category

                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                $locationProvider.html5Mode true
                # Bind routes to the controllers
                $routeProvider
                    .when('/', redirectTo: '/categories/survey')
                    .when('/categories/:category',
                        controllerProvider:  (parm)-> 
                            return getCategory(parm.category).controller
                        templateUrl: (parm)-> 
                            return getCategory(parm.category).templateUrl
                    )

    ])