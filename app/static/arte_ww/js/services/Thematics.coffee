angular.module('arte-ww.services').service 'Survey', [
        '$resource', '$routeParams', 
        ($resource, $routeParams)->
            params = 
                thematic: $routeParams.thematic
            $resource '/api/survey/', params,
                get: 
                    url: '/api/survey/:thematic_id'
                all:
                    method: 'GET'
                    isArray: yes

    ]

