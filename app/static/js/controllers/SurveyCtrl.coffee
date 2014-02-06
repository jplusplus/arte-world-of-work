class SurveyCtrl
    @$inject: [ '$scope', 'Survey' ]
    constructor: ($scope, Survey) ->
        console.log "SurveyCtrl.init"
        $scope.elements = [{
            
        }]
        $scope.currentElement = 0

    skip: -> 


angular.module('arte-ww') 
    .controller('SurveyCtrl', SurveyCtrl)  