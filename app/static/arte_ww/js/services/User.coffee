class UserService
    @$inject: ['$http']

    constructor: (@$http) ->

    post: =>
        request =
            method : 'POST'
            url : '/api/user/'

        @$http request

(angular.module 'arte-ww.services').service 'User', UserService