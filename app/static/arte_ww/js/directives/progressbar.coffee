# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 11:51:02
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

angular.module('arte-ww').directive 'progressbar', ['UserPosition', 'Thematic', 'ElementsWrapper', 'utils',
    (UserPosition, Thematic, ElementsWrapper, utils) ->
        directive =
            restrict: "A"
            link: (scope, elem) ->
                thematicElements = []
                elements = 0

                positions =
                    global : 0
                    thematic : 0
                    element : 0

                updateBarWidth = (position) ->
                    if elements > 0
                        percent = "#{position * 100 / elements}%"
                    else
                        percent = 0
                    elem[0].style.width = percent
                    elem[0].innerHTML = percent

                scope.$watch (=>
                    if Thematic.positionList?
                        Thematic.positionList.elements.length
                    else
                        0
                ), ((val) =>
                    if val is 0 then return

                    thematicElements = _.map Thematic.positionList.elements, (e) -> e.elements.length
                    elements = _.reduce thematicElements, ((it, elem) => it + elem), 0
                    updateBarWidth positions.global
                ), yes

                updatePosition = =>
                    positions.global = 0
                    if positions.thematic > 0
                        for i in [0..(positions.thematic - 1)]
                            positions.global += thematicElements[i]
                    positions.global += positions.element
                    updateBarWidth positions.global

                scope.$watch (=> do ElementsWrapper.current), (newElement) ->
                    return unless newElement
                    if newElement and newElement.type is 'question'
                        index = ElementsWrapper.allQuestions().indexOf newElement
                        positions.element = index
                        do updatePosition

                scope.$watch (=> do UserPosition.thematicPosition), (newPosition, oldPosition) ->
                    positions.thematic = newPosition
                    do updatePosition
]
