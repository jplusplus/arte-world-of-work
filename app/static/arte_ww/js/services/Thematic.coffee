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
        # we will first load a thematic list in that array. It will help us 
        # to guess a thematic ID by its position  
        @metaList  = [] 

        # first (fast) request where we get the list of thematics and their positions 
        $http(@listConfig).success (data)=>
            @positionList = @userPosition.createWrapper(data)
            # watches 
            @rootScope.$watch =>
                    @userPosition.thematicPosition()
                , @onThematicPositionChanged

        @nestedThematics = $resource @resourceConfig.url, {id: 1}, 
            @resourceConfig.actions

    # API method / internal functions 
    all: (cb)=> 
        return @nestedThematics.all cb

    get: (params, cb)=>
        @nestedThematics.get params, (thematic)=>
            @loadedThematics[thematic.id] = thematic
            cb(thematic)

    getAt: (position, cb)=>
        return unless @positionList

        id = @positionList.getAt(position).id # we have to check thematic list 
        thematic = @loadedThematics[id]
        if thematic?
            cb(thematic)
        else
            @get(id: id, cb)

    onThematicPositionChanged: (position)=>
        @getAt position, (thematic)=> 
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
        