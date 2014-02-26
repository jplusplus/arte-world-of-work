class SurveyCtrl
    @$inject: ['$scope', 'Thematic', 'UserPosition', 'utils']
    constructor: (@scope, @thematicService, @userPosition, utils)->
        @states = utils.states.survey
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.survey =  
            state   : 0
            states  : @states
        # User's position functions
        @scope.elementPosition = => @userPosition.elementPosition() + 1
        @scope.elementsCount   = => @thematicService.current().elements.length
        # Returns the classes of the given questions
        @scope.getQuestionClasses = (question)->             
            'survey-element--with-columns': question.choices.length >= 4
            'survey-element--with-media'  : question.media isnt null
            


angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


