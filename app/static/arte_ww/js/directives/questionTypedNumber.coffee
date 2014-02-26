angular.module('arte-ww').directive 'questionTypedNumber', [
    'Answer'
    (answerService)->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-typed-number.html"
            link: (scope, elem, attrs)->
                scope.question        = scope.$parent.element
                # We need to put answer into a sub-object to be edited by noui directive
                scope.question.answer = (scope.question.max_number - scope.question.min_number)/2
]
