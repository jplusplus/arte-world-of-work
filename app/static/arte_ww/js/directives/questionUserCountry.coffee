angular.module('arte-ww').directive 'questionUserCountry', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-user-country.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
]
