angular.module('arte-ww').directive 'questionSelection', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-selection.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
]
