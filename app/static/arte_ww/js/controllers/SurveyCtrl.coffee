class SurveyCtrl
    @$inject: ['$scope', 'Thematic']
    constructor: (@scope, @Thematic)->
        
        @scope.survey =
            state: 0
            thematic: null

        @scope.$watch UserPosition.currentThematic, 'onThematicChanged'

        _.extend @scope, 
            previous: @previousThematic
            next: @previousThematic

    previousThematic: => 
        UserPosition.previousThematic()

    nextThematic: => 
        UserPosition.nextThematic() 

angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl