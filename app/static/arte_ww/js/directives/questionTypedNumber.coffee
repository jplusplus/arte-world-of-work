angular.module('arte-ww').directive 'questionTypedNumber', [
    'Answer'
    (answerService)->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-typed-number.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element                
                # We need to put answer into a sub-object to be edited by noui directive
                scope.question.answer = scope.answer or (scope.question.max_number - scope.question.min_number)/2
                scope.step            = ~~( scope.question.max_number * 0.1 )
                # Reflect the question.answer value to scope.answer
                scope.$watch "question.answer", (answer)->                  
                    if answer?
                        scope.answer = answer 
]
