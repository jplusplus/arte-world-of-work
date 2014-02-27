angular.module('arte-ww').directive 'questionBoolean', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-boolean.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element

                scope.submit = (choice)->
                    answerParams = 
                        question: scope.question.id
                        value: choice.id

                    scope.submitAnswer(answerParams).success(scope.next)
]


