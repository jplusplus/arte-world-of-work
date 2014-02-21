angular.module('arte-ww').directive 'questionUserGender', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-radio.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
                scope.submit = (choice)->
                    scope.answer = choice
                    
                    answerParams = 
                        question: scope.question.id
                        value: choice.value

                    scope.submitAnswer(answerParams)
                        .success(->
                            console.log 'success ! '
                            scope.next()
                        )
                        .error((data)->
                            console.log 'error !', data
                        )



]
