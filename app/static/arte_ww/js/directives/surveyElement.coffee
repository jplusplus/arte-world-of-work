TYPOLOGIES =
    BOOLEAN       : 'boolean'
    RADIO_TYPE    : 'media_radio'
    SELECTION_TYPE: 'media_selection'
    TYPED_NUMBER  : 'typed_number'
    USER          :
        AGE    : 'user_age'
        COUNTRY: 'user_country'
        GENDER : 'user_gender'


angular.module('arte-ww').directive 'surveyElement', [
    'Answer'
    (answerService)->
        directive = 
            restrict: "AE"
            replace: yes
            templateUrl: "partial/directives/survey-element.html"
            controller: ['$scope', 'Answer', '$timeout', (scope, answerService, $timeout) ->
                scope.submitAnswer = (answer, delay=yes)->
                    answer = answer ? scope.answer
                    answerParams = 
                        question: scope.element.id 
                        value: answer

                    # Save the answer
                    answerService.answer answerParams
                    # Add a light duration before switching to the next step
                    duration = if delay then 500 else 0
                    # Add go to the new question instantanetly
                    $timeout(scope.next, duration)
                    
            ]

            link: (scope, elem, attrs)->
                # let the template use choices typologies for sub-directive selection
                scope.TYPOLOGIES = TYPOLOGIES
                scope.$watch -> 
                        scope.$eval(attrs.surveyElement)
                    , (element)->
                        scope.element = element
                

                scope.$watch ->
                        return unless scope.element
                        answerService.getAnswerForQuestion scope.element.id 
                    , (previousAnswer)->
                        return unless previousAnswer
                        scope.answer = previousAnswer.value
                             

]