class SurveyCtrl
    @$inject: [ '$scope', 'Survey' ]
    constructor: ($scope, Survey) ->
        $scope.questions = Survey.get thematic: 1


angular.module('arte-ww') 
    .controller('SurveyCtrl', SurveyCtrl)