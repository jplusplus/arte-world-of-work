### 
Key responsibilities of ThematicServices
    - handle different thematic loading
### 
class ThematicService
    @$inject: ['$rootScope', '$routeParams', '$http', '$resource']

    constructor: (@rootScope, @routeParams, $http, $resource)-> 
        # every loaded thematic will be contained inside this object 
        @loadedThematics = {}
        # we will first load a thematic list in that array. It will help us 
        # to guess a thematic ID by its position  
        @metaList  = [] 

        $http(@listConfig).success (data)=>
            @list = data

        @nestedThematics = $resource @resourceConfig.url, {id: 1}, 
            @resourceConfig.actions

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

    # API method / internal functions 
    all: (cb)=> 
        return @nestedThematics.all cb

    get: (params, cb)=>
        @nestedThematics.get params, (thematic)=>
            @loadedThematics[thematic.id] = thematic
            cb(thematic)

    getAt: (position, cb)=>
        return unless @list
        id = @list[position].id # we have to check thematic list 
        thematic = @loadedThematics[id]
        if thematic
            cb(thematic)
        else
            @get(id: id, cb)

angular.module('arte-ww.services').service 'Thematic', ThematicService
        