# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-04-03 17:12:53
# Last Modified time: 2014-04-10 12:09:10
# -----------------------------------------------------------------------------
# This file is part of World of Work
#
#   World of Work, a study of the european youth and its perception of the world of work
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

class ThematicCtrl
    # Key responsibilities of ThematicCtrl
    #     - handle different thematic states: thematic introduction
    #     - handle navigation around current thematic elements
    @$inject: [
        # angular dependencies 
        '$scope'
        '$sce'
        # internal dependencies 
        'utils'
        'UserPosition'
        'Thematic'
        'Answer'
        'Feedback'
        'ElementsWrapper'
    ]

    constructor: ( @scope, @sce, @utils, @userPosition, @thematicService, @Answer, @feedbackService, @elementsWrapper)->
        # ---------------------------------------------------------------------
        # Class attributes
        # ---------------------------------------------------------------------
        @states = @utils.states.thematic
        
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            state: @states.LANDING,
            states: @states,
            thematic: @thematicService
            # function binding
            

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            next: @skipElement,
            previous: @previousElement
            currentState: @currentState
            elements: @elements
            currentElement: => @currentElement
            start: =>
                @utils.authenticate @startThematic
            letsgo: @letsgo

        # ---------------------------------------------------------------------
        # watches
        # ---------------------------------------------------------------------
        @scope.$watch (=>
            @userPosition.positions
        ), (newdata, olddata) =>
            if newdata.elementPosition? and newdata.thematicPosition? and @scope.state is @states.LANDING
                if newdata.thematicPosition is olddata.thematicPosition
                    if (newdata.elementPosition isnt 0) or newdata.thematicPosition isnt 0
                        @scope.letsgo true
        , yes

        @scope.$watch 'thematic.currentThematic', @onThematicChanged
        @scope.$watch => 
                @elementsWrapper.currentElement
            , @onElementChanged


    elements: => @elementsWrapper.all()

    # -------------------------------------------------------------------------
    # State manipulation/test methods
    # -------------------------------------------------------------------------
    currentState: (state)=>
        # getter/setter for the current state of the survey
        # See @utils.states.thematic for the different possible states
        if state?
            @scope.state = state
            @userPosition.currentState @scope.state
        @scope.state

    isLanding : => @currentState() == @states.LANDING
    isIntro   : => @currentState() == @states.INTRO
    isElements: => @currentState() == @states.ELEMENTS
    isDone    : => @isElements() and @userPosition.elementPosition() >= @elements().length - 1

    # -------------------------------------------------------------------------
    # Navigation methods
    # -------------------------------------------------------------------------
    letsgo: (skipIntro=false) =>
        if (do @userPosition.elementPosition is 0) and not skipIntro
            @currentState @states.INTRO
        else
            @currentState @states.ELEMENTS

    startThematic: =>
        # Launch the current thematic and show its elements. Should be called 
        # to end thematic introduction
        @currentState(@states.ELEMENTS)

    skipElement: (skipped=false) =>
        # go to the next element and delete the current element's answer if we 
        # skipped it (skipped attribute set to true)
        if skipped
            @Answer.deleteAnswerForQuestion @currentElement.id
        
        if @elementsWrapper.hasNextElement()
            @userPosition.nextElement()
        else if @isDone()
            @setNextThematic()
        else
            @currentState(@states.OUTRO)

    previousElement: =>
        # like @skipElement but in opposite direction.
        if @isIntro()
            @userPosition.previousThematic()
            @currentState(@states.ELEMENTS)
        else if @elementsWrapper.hasPreviousElement()
            @userPosition.previousElement()
        else
            @currentState(@states.INTRO)

    setNextThematic: =>
        # go to the next thematic
        @userPosition.nextThematic()
        (do @userPosition.thematicPosition)
        if (do @userPosition.thematicPosition) < @thematicService.count()
            @currentState @states.LANDING
        else
            @scope.$parent.setState @utils.states.survey.OUTRO

    # -------------------------------------------------------------------------
    # watches callbacks 
    # -------------------------------------------------------------------------
    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        if (typeof thematic.intro_description) is typeof String
            _.extend @scope.thematic.currentThematic,
                intro_description: @sce.trustAsHtml(thematic.intro_description)
        
        # special case for "You" thematic to skip the landing page. 
        # !! DO NOT CHANGE !!
        if @userPosition.thematicPosition() is 0
            do @letsgo


    onElementChanged: (elem, old_elem)=>
        elem_pos = @userPosition.elementPosition()
        out_of_range = elem_pos >= @elements().length 
        # # security check, to pass to next thematic if last element is undefined
        # # this undefined value can occur if we wanted to show a feedback for the 
        # # last element of the current thematic
        if old_elem and !elem and @isDone()
            @setNextThematic()

        if elem?
            @currentElement = elem
        # if elem and !@isElements() and !@isIntro()
        #     @currentState @states.ELEMENTS



angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl