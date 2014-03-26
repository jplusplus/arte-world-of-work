angular.module('arte-ww').directive 'questionUserCountry', [
    'Country'
    (countryService)->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-user-country.html"
            link: (scope, elem, attrs)->
                scope.question  = scope.$parent.element
                scope.countries = countryService 

                scope.$watch '$parent.element', -> scope.question = scope.$parent.element               

]
