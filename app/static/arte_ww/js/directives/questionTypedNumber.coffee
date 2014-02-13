angular.module('arte-ww').directive 'questionTypedNumber', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-typed-number.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
]
