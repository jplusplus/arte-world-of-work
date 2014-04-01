### 
Key responsibilities of ThematicServices
    - handle different thematic loading
### 

class ThematicService
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
    
    constructor: (@rootScope, @routeParams, @http, $resource, $translate, @userPosition, @utils, @Xiti)-> 
        # every loaded thematic will be contained inside this object 
        @loadedThematics = {}
        
        @getPositions =>
            @rootScope.$watch (=> do @userPosition.thematicPosition), @onThematicPositionChanged

        @nestedThematics = $resource @resourceConfig.url, {id: 1}, 
            @resourceConfig.actions

        @rootScope.$watch -> 
                $translate.use()
            , @getPositions

    count: ()=> @positions().length

    positions: => if @positionList then @positionList.all() else []

    # API method / internal functions 
    all: (cb)=> @nestedThematics.all cb

    getPositions: (cb)=>
        @http(@listConfig).success (data)=>
            @positionList = @userPosition.createWrapper(data)
            if cb and typeof cb is Function
                cb(data)

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

    onThematicPositionChanged: (position)=>        
        @getAt position, (thematic)=> 
            # Monitor user activity
            @Xiti.loadPage @rootScope.currentCategory(), thematic.slug
            # Update current thematic
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
        