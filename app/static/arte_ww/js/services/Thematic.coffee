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
        'UserPosition',
        'utils'
    ]
    
    constructor: (@rootScope, @routeParams, $http, $resource, @userPosition, @utils)-> 
        # every loaded thematic will be contained inside this object 
        @loadedThematics = {}
        # first (fast) request where we get the list of thematics and their positions 
        $http(@listConfig).success (data)=>
            @positionList = @userPosition.createWrapper(data)
            # watches 
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

    onThematicPositionChanged: (position)=>        
        @getAt position, (thematic)=> @currentThematic = thematic

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
        