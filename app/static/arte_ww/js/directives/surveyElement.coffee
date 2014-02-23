TYPOLOGIES =
    USER:
        GENDER: 'user_gender'
        AGE: 'user_age'
        COUNTRY: 'user_country'
    TYPED_NUMBER: 'typed_number'
    RADIO_TYPES: ['boolean', 'text_radio', 'media_radio']
    SELECTION_TYPES: ['text_selection', 'media_selection']




angular.module('arte-ww').directive 'surveyElement', [
    'Answer'
    (answerService)->
        directive = 
            restrict: "AE"
            replace: yes
            templateUrl: "partial/directives/survey-element.html"
            controller: ['$scope', 'Answer', (scope, answerService) ->
                scope.submitAnswer = (answer)->
                    answer = answer ? scope.survey.answer
                    answerParams = 
                        question: scope.element.id 
                        value: answer

                    answerService.answer answerParams,
                        success: ->
                            scope.next()
                        error: (msg)->
                            console.error(msg)
            ]

            link: (scope, elem, attrs)->
                scope.survey = 
                    answer: undefined
                # let the template use choices typologies for sub-directive selection
                scope.TYPOLOGIES = TYPOLOGIES
                scope.$watch -> 
                        scope.$eval(attrs.surveyElement)
                    , (element)->
                        scope.element = element
                        if element.type == 'question'
                            previousAnswer = answerService.getAnswerForQuestion element.id 
                            scope.survey.answer = previousAnswer.value if previousAnswer
                             

]