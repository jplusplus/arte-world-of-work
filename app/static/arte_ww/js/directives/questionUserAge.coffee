angular.module('arte-ww').directive 'questionUserAge', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-user-age.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element                
                # We need to put answer into a sub-object to be edited by noui directive
                scope.question.answer = scope.answer or 25
                # Reflect the question.answer value to scope.answer
                scope.$watch "question.answer", (answer)->                  
                    if answer?
                        scope.answer = answer 

                scope.$watch '$parent.element', -> scope.question = scope.$parent.element               
                
]
