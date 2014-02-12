class SurveyCtrl
    @$inject: ['$scope', 'Thematic', 'UserPosition']
    constructor: (@scope, @thematic, @userPosition)->
        # scope function binding - public API of this controller
        @scope.survey =  
            state: 0
            thematic: @thematic.currentThematic


angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl