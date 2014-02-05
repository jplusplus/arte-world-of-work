class SurveyCtrl
    @$inject: [ '$scope', 'Survey' ]
    constructor: ($scope, Survey) ->
        console.log "SurveyCtrl.init"
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

angular.module('arte-ww') 
.controller('SurveyCtrl', SurveyCtrl)  