class SurveyCtrl
    @$inject: ['$scope', '$sce', 'Thematic', 'UserPosition', 'utils']
    constructor: (@scope, @sce, @thematicService, @userPosition, utils)->
        @scope.$watch (=>
            @userPosition.positions
        ), (newdata, olddata) =>
            if newdata.elementPosition? and newdata.thematicPosition? and @scope.survey.state is 0
                if (newdata.elementPosition isnt 0) or newdata.thematicPosition isnt 0
                    do @scope.start
        , yes

        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @states = utils.states.survey

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

        @scope.start = =>
            @thematicService.onThematicPositionChanged do @userPosition.thematicPosition
            @scope.survey.state = @scope.survey.states.DOING

        @scope.startButton = =>
            if (do @userPosition.thematicPosition is 0) and (do @userPosition.elementPosition is 0)
                'Start'
            else
                'Continue'

angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


