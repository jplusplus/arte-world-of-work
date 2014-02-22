TYPOLOGIES =
    USER:
        GENDER: 'user_gender'
        AGE: 'user_age'
        COUNTRY: 'user_country'
    TYPED_NUMBER: 'typed_number'
    RADIO_TYPES: ['boolean', 'text_radio', 'media_radio']
    SELECTION_TYPES: ['text_selection', 'media_selection']




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
                # let the template use choices typologies for sub-directive selection
                scope.TYPOLOGIES = TYPOLOGIES
                scope.$watch -> 
                        scope.$eval(attrs.surveyElement)
                    , (element)->
                        scope.element = element

]