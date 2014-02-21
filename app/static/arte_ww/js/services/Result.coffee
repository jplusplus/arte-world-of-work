class ResultService
    @$inject: ['$http']

    constructor: (@$http) ->

    get: (params, cb) =>
        request =
            method : 'GET'
            url : "/api/questions/#{params.id}/result"
            params : params.filters
        (@$http request).success cb

    

(angular.module 'arte-ww.services').service 'Result', ResultService