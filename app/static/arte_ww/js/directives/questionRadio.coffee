angular.module('arte-ww').directive 'questionRadio', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-radio.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element

                scope.submit = (choice)->
                    answerParams = 
                        question: scope.question.id
                        value: choice.id

                    scope.submitAnswer(answerParams)
                        .success(->
                            console.log 'success ! '
                            scope.next()
                        )
                        .error((data)->
                            console.log 'error !', data
                        )


                

]


