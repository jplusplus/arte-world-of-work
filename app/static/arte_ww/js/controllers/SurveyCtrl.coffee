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

        @scope.setState = (state) =>
            @scope.survey.state = state

        @scope.survey =
            state   : 0
            states  : @states
        # User's position functions
        @scope.elementPosition = => @userPosition.elementPosition() + 1
        @scope.elementsCount   = => @thematicService.current().elements.length
        @scope.prepareVineUrl  = (url)=> @sce.trustAsResourceUrl("#{url}/embed/postcard")

        # Returns the classes of the given questions
        @scope.getQuestionClasses = (question)->
            'survey-element--with-columns'   : question.choices && question.choices.length >= 4
            'survey-element--without-columns': not(question.choices && question.choices.length >= 4)
            'survey-element--with-media'     : question.media isnt null
            'survey-element--without-media'  : not(question.media isnt null)
            'survey-element--choice-media'   : question.has_medias
            'survey-element--icon-mode'      : (question.has_medias && question.choices.length > 3) || (question.media_type and question.media_type == "icon")

        @scope.start = =>
            @thematicService.onThematicPositionChanged do @userPosition.thematicPosition
            if (do @userPosition.thematicPosition) >= @thematicService.positionList.elements.length
                @scope.survey.state = @scope.survey.states.OUTRO
            else
                @scope.survey.state = @scope.survey.states.DOING

angular.module('arte-ww').controller 'SurveyCtrl', SurveyCtrl


