class ResultService
    @$inject: ['$http']

    constructor: (@$http) ->

    get: (params, cb) =>
        request =
            method : 'GET'
            url : "/api/questions/#{params.id}/results"
            params : params.filters
        (@$http request).success cb

    post: (params, cb) =>
        request =
            method: 'POST'
            url : '/api/answers/#{params.question.id}'
            data: params.value
            

(angular.module 'arte-ww.services').service 'Result', ResultService