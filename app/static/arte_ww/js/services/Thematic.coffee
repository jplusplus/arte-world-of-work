angular.module('arte-ww.services').service 'Thematic', [
        '$resource', '$routeParams', 
        ($resource, $routeParams)->
            params = 
                thematic: $routeParams.thematic
            $resource '/api/thematics/', params,
                get: 
                    url: '/api/thematics/:thematic_id'
                all:
                    method: 'GET'
                    isArray: yes

    ]

