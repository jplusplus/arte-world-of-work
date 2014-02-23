angular.module('arte-ww').directive 'questionUserAge', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-radio.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
]
