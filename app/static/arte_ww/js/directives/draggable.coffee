# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 12:10:51
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

angular.module('arte-ww').directive "draggable", ['$document', ($document) ->
  (scope, element, attr) ->    
    startX = startY = 0
    x = y = 0
    # Prevent default dragging of selected content
    mousemove = (event) ->
      y = event.pageY - startY
      x = event.pageX - startX
      element.css
        top:  y + "px"
        left: x + "px"

    mouseup = ->
      $document.unbind "mousemove", mousemove
      $document.unbind "mouseup", mouseup
      if attr.restore?
        x = y = 0
        element.animate { top: 0, left: 0 }, 400

    element.css "position", "relative" if element.css("position") is "static"

    element.on "mousedown", (event) ->
      event.preventDefault()   
      startX = event.pageX - x
      startY = event.pageY - y
      $document.on "mousemove", mousemove
      $document.on "mouseup", mouseup
]
