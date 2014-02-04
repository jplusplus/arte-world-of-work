class SurveyService
    @$inject: ['$resource', '$routeParams']
    constructor: ($resource, $routeParams)->
        params = 
            thematic: $routeParams.thematic

        $resource '/api/survey/:thematic', params,
            # read only
            post: null
            update: null
            patch: null


angular.module('arte-ww.services').service 'Survey', SurveyService