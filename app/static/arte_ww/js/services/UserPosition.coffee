# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-04-03 17:51:37
# Last Modified time: 2014-04-10 12:12:53
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

class PositionsObject
    constructor: (elements, @utils)->
        elements = @wrapElements(elements)
        @updateElements(elements)

    get_pos = (el)-> 
        return el unless el
        el.position

    set_index_as_pos = (el,i)-> 
        return el unless el
        el.position = i
        el

    makeElementPositionsUnique:(elements)=>
        elements  = _.sortBy elements, get_pos
        elements  = _.map    elements, set_index_as_pos
        elements

    updateElements: (elements)=>
        elements  = elements or @elements
        elements  = @makeElementPositionsUnique(elements)
        elements  = @updatePositions(elements)
        @elements = elements


    updatePositions:(elements)=>
        @positions =  _.map(elements, get_pos)
        elements

    positionAt: (i)=> @positions[i]

    getAt: (i)=> _.findWhere @elements, position: @positionAt(i)

    insertAt: (i, el)=>
        left_part   = _.first( @elements, i )
        right_part  = _.rest(  @elements, i )
        if left_part.length > 0
            el.position = _.last( left_part ).position + 1
        else
            el.position = _.first( right_part ).position
        _.each right_part, (el)-> el.position += 1
        elements  = _.union left_part, [el], right_part
        @updateElements(elements)

    count: => @elements.length

    wrapElem: (el)=>
        return el unless el.type?
        if el.type is 'question'
            el = @utils.wrapQuestion(el)
        else if el.type is 'feedback'
            el = @utils.wrapFeedback(el)
        el

    wrapElements: (elements)=> _.map elements, @wrapElem

    all: => @elements

class UserPositionService
    @$inject: ['$rootScope', '$http', 'utils']

    state: undefined
    positions:
        lastElementPosition: undefined
        thematicPosition: undefined
        elementPosition: undefined

    constructor: (@rootScope, @$http, @utils) ->
        # Notify rootScope to display a loading spinner
        @rootScope.isUserLoading = yes 

        @utils.authenticate (=>
            request =
                url : '/api/my-position'
                method : 'GET'
            ((@$http request).success (data) =>
                # Disabled loading spinner
                @rootScope.isUserLoading = no
                
                @positions =
                    thematicPosition : data.thematic_position
                    elementPosition : data.element_position
            ).error =>
                # Disabled loading spinner  
                @rootScope.isUserLoading = no

                @positions =
                    thematicPosition : 0
                    elementPosition : 0
        ), no

    currentState: (state) =>
        if state?
            @state = state
        @state

    sendPosition: () =>
        request =
            url : '/api/my-position/'
            method : 'PATCH'
            data :
                thematic_position : @positions.thematicPosition
                element_position : @positions.lastElementPosition
        @$http request

    thematicPosition: (position) =>
        if position?
            @positions.thematicPosition = position
            do @sendPosition
        @positions.thematicPosition

    lastElementPosition: (position)=>
        if position?
            @positions.lastElementPosition = position
            do @sendPosition
        @positions.lastElementPosition

    elementPosition:  (position, save=true) =>
        if position?
            @positions.elementPosition = position
            if save
                do @sendPosition
        @positions.elementPosition

    nextThematic: =>
        @currentState( @utils.states.thematic.LANDING )
        @elementPosition 0, false
        @thematicPosition @positions.thematicPosition + 1

    previousThematic: =>
        @currentState( @utils.states.thematic.ELEMENTS )
        @thematicPosition @positions.thematicPosition - 1

    nextElement: (save = true) =>
        @elementPosition @positions.elementPosition + 1, false

    previousElement: (save = true) =>
        @elementPosition @positions.elementPosition - 1, false

    createWrapper: (elements)-> return new PositionsObject(elements, @utils)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService