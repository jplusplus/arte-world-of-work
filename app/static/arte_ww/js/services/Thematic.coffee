### 
Key responsibilities of ThematicServices
    - handle different thematic loading
### 
class ThematicService

    @$inject: ['$resource', '$routeParams']
    
    constructor: (@resource, @routeParams)-> 
        @baseURL  = '/api/thematics/:thematicId'
        @defaultParams = 
            thematicId: null 

        @actions = 
            all: 
                method: 'GET'
                isArray: true

        @resource = @resource @baseURL, @defaultParams, @actions

    all: (cb)=> 
        return @resource.all
    get: (thematicId, cb)=>
        return @resource.get thematicId, cb 


angular.module('arte-ww.services').service 'Thematic', ThematicService
        