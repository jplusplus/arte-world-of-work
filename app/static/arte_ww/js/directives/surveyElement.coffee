angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "AE"
            replace: yes
            templateUrl: "partial/directives/survey-element.html"
            controller: ['$scope', 'Answer', (scope, answerService) ->
                scope.submitAnswer = (answer)->
                    answerParams = 
                        question: scope.element.id 
                        value: answer

                    answerService.post(answerParams)
                        .success(->
                            scope.next()
                        )
                        .error((msg)->
                            console.error(msg)
                        )
            ]

            link: (scope, elem, attrs)->
                scope.$watch -> 
                        scope.$eval(attrs.surveyElement)
                    , (element)->
                        scope.element = element

]