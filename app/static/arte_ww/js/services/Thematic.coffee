# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-04-01 18:54:37
# Last Modified time: 2014-04-10 12:12:33
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

class ThematicService
    # Key responsibilities of ThematicServices
    #    - handle different thematic loading
    
    # Dependencies injection
    @$inject: [
        '$rootScope', 
        '$routeParams', 
        '$http', 
        '$resource',
        '$translate', 
        'UserPosition',
        'utils',
        'Xiti'
    ]
    
    constructor: (@rootScope, @routeParams, @http, $resource, @translate, @userPosition, @utils, @Xiti)-> 
        # every loaded thematic will be contained inside this object 
        @loadedThematics = {}

        @http(@listConfig).success (data)=>
            @positionList = @userPosition.createWrapper(data)
            @rootScope.$watch (=> do @userPosition.thematicPosition), @onThematicPositionChanged

        @nestedThematics = $resource @resourceConfig.url, {id: 1}, 
            @resourceConfig.actions

    count: ()=> @positions().length

    positions: => if @positionList then @positionList.all() else []

    # API method / internal functions 
    all: (cb)=> @nestedThematics.all cb

    get: (params, cb)=>
        # Notify rootScope to display a loading spinner
        @rootScope.isThematicLoading = yes 
        @nestedThematics.get params, (thematic)=>
            @loadedThematics[thematic.id] = thematic
            # Disabled loading spinner
            @rootScope.isThematicLoading  = no 
            cb(thematic)

    getAt: (position, cb)=>
        return unless @positionList
        positionAt = @positionList.getAt(position)             
        if positionAt? and positionAt.id?
            if @loadedThematics[positionAt.id]?
                cb @loadedThematics[positionAt.id]        
            else
                @get(id: positionAt.id, cb)

    onThematicPositionChanged: (position, triggerXiti=yes)=>        
        @getAt position, (thematic)=> 
            if triggerXiti
                # Monitor user activity
                @Xiti.loadPage @rootScope.currentCategory(), thematic.slug
                # Update current thematic
                @currentThematic = thematic
            else
                @rootScope.safeApply =>
                    @currentThematic = thematic

    current: => @currentThematic



    #--------------------------------------------------------------------------
    # Configuration objects & static definitions 
    #--------------------------------------------------------------------------

    listConfig: 
        url: '/api/thematics/'
        method: 'GET'

    # configuration of nested thematics resource. It's the resource that will
    # be used to load individual thematics
    resourceConfig:
        url: '/api/thematics-nested/:id/'
        actions:
            all:
                method: 'GET'
                isArray: yes
                params:
                    id: null

angular.module('arte-ww.services').service 'Thematic', ThematicService
        