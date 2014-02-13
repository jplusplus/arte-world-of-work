class SurveyCtrl
    @$inject: ['$scope', 'Thematic', 'UserPosition', 'utils']
    constructor: (@scope, @thematicService, @userPosition, utils)->
        @states = utils.states.survey
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.survey =  
            state: 0
            states: @states

angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


