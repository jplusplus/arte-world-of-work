angular.module('arte-ww.services').service 'Survey', [
        '$resource', '$routeParams', 
        ($resource, $routeParams)->
            params = 
                thematic: $routeParams.thematic
            $resource '/api/survey/:thematicId', params

    ]

