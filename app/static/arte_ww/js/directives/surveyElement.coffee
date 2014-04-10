# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-27 16:19:29
# Last Modified time: 2014-04-10 11:52:25
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

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
                scope.element = scope.$eval(attrs.surveyElement)

                scope.$watch ->
                        return unless scope.element
                        answerService.getAnswerForQuestion scope.element.id 
                    , (previousAnswer)->
                        return unless previousAnswer
                        scope.answer = previousAnswer.value
                             

]