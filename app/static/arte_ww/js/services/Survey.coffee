angular.module('arte-ww.services').service 'Thematics', [
        '$resource', '$routeParams', 
        ($resource, $routeParams)->
            params = 
                thematic: $routeParams.thematicId

            $resource '/api/thematics/', params,
                get: 
                    url: '/api/thematics/:thematic_id'
                all:
                    method: 'GET'
                    isArray: yes

    ]

