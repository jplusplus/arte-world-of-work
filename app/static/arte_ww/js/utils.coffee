class Utils
    @$inject: ['$http', '$cookies', 'User']

    constructor: (@$http, @$cookies, @User) ->

    # -------------------------------------------------------------------------
    # Utility service for front-end application
    #
    # attributes:
    #    - states: common state name / value shared accross components
    # -------------------------------------------------------------------------
    states:
        survey:
            INTRO: 0
            DOING: 1
            OUTRO: 2
        thematic:
            LANDING : 0
            INTRO   : 1
            ELEMENTS: 2

    authenticate: (callback, create = yes) =>
        createNewUser = =>
            (do @User.post).success (data) =>
                @$cookies['apitoken'] = data.token
                do callback
        if not @$cookies['apitoken']?
            if create
                do createNewUser
            else
                do callback
        else
            request =
                method : 'POST'
                url : '/api/verify-token/'
            ((@$http request).success =>
                do callback
            ).error (error, status) =>
                if status is 401
                    delete @$cookies['apitoken']
                    if create
                        do createNewUser
                    else
                        do callback


angular.module('arte-ww.utils').service('utils', Utils)