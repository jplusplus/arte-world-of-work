# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-26 19:38:00
# Last Modified time: 2014-04-10 11:59:08
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

class SurveyCtrl
    @$inject: ['$scope', '$sce', 'Thematic', 'ElementsWrapper', 'UserPosition', 'utils']
    constructor: (@scope, @sce, @thematicService, @elementsWrapper, @userPosition, utils)->
        @scope.$watch (=>
            @userPosition.positions
        ), (newdata, olddata) =>
            if newdata.elementPosition? and newdata.thematicPosition? and @scope.survey.state is 0
                if (newdata.elementPosition isnt 0) or newdata.thematicPosition isnt 0
                    do @scope.start
        , yes

        @thematicService.onThematicPositionChanged do @userPosition.thematicPosition

        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @states = utils.states.survey

        @scope.setState = (state) =>
            @scope.survey.state = state

        @scope.survey =
            state   : 0
            states  : @states
        # User's position functions
        @scope.elementPosition = => 
            current = @elementsWrapper.currentElement
            if current.type is 'question'
                index = @elementsWrapper.allQuestions().indexOf current
                return index + 1  

        @scope.elementsCount   = => 
            @elementsWrapper.allQuestions().length 

        @scope.prepareVineUrl  = (url)=> @sce.trustAsResourceUrl("#{url}/embed/postcard")

        # Returns the classes of the given questions
        @scope.getQuestionClasses = (question)->
            'survey-element--with-columns'   : question.media is null && question.choices && question.choices.length >= 4
            'survey-element--without-columns': not(question.media is null && question.choices && question.choices.length >= 4)
            'survey-element--with-media'     : question.media isnt null
            'survey-element--without-media'  : not(question.media isnt null)
            'survey-element--choice-media'   : question.has_medias
            'survey-element--icon-mode'      : (question.has_medias && question.choices.length > 3) || (question.media_type and question.media_type == "icon")

        @scope.start = =>
            @thematicService.onThematicPositionChanged do @userPosition.thematicPosition
            if (do @userPosition.thematicPosition) >= @thematicService.count()
                @scope.survey.state = @scope.survey.states.OUTRO
            else
                @scope.survey.state = @scope.survey.states.DOING

angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


