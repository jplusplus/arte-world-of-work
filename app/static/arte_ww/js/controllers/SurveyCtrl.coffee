class SurveyCtrl
    @$inject: ['$scope']

    constructor: (@scope)->
        @scope.survey =
            state: 0

angular.module 'arte-ww'
    .controller 'SurveyCtrl', SurveyCtrl