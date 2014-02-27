class SurveyCtrl
    @$inject: ['$scope', '$sce', 'Thematic', 'UserPosition', 'utils']
    constructor: (@scope, @sce, @thematicService, @userPosition, utils)->
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
        @scope.prepareVineUrl  = (url)=> @sce.trustAsResourceUrl("#{url}/embed/postcard")

        # Returns the classes of the given questions
        @scope.getQuestionClasses = (question)->             
            'survey-element--with-columns': question.choices && question.choices.length >= 4
            'survey-element--with-media'  : question.media isnt null
            'survey-element--choice-media': question.has_medias
            'survey-element--icon-mode'   : (question.has_medias && question.choices.length > 3) || (question.media_type and question.media_type == "icon")
            


angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


