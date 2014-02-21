class AnswerService
    @$inject: ['$http']

    constructor: (@$http) ->

    get: (params, cb) =>
        request =
            method : 'GET'
            url : "/api/my-answers/"
        (@$http request).success cb

    post: (params, cb) =>
        request =
            method: 'POST'
            url : '/api/answers/'
            data: params
        (@$http request).success cb
            

(angular.module 'arte-ww.services').service 'Answer', AnswerService