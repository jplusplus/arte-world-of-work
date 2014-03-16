### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$rootScope', '$scope', '$sce', 'utils', 'UserPosition', 'Thematic', 'Answer' ]

    constructor: (@rootScope, @scope, @sce, @utils, @userPosition, @thematicService, @Answer)->
        @scope.$watch (=>
            @userPosition.positions
        ), (newdata, olddata) =>
            if newdata.elementPosition? and newdata.thematicPosition? and @scope.state is @states.LANDING
                if newdata.thematicPosition is olddata.thematicPosition
                    if (newdata.elementPosition isnt 0) or newdata.thematicPosition isnt 0
                        @onElementPositionChanged do @userPosition.elementPosition
                        @scope.letsgo true
        , yes

        # ---------------------------------------------------------------------
        # Class attributes
        # ---------------------------------------------------------------------
        @states = @utils.states.thematic
        
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            state: @states.LANDING,
            states: @states,
            thematic: @thematicService

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            next: @skipElement,
            previous: @previousElement
            currentState: @currentState
            start: =>
                @utils.authenticate @startThematic
            letsgo: @letsgo

        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @scope.$watch 'thematic.currentThematic', @onThematicChanged 
        @scope.$watch => 
                @userPosition.elementPosition()
            , @onElementPositionChanged

    letsgo: (skipIntro=false) =>
        if (do @userPosition.elementPosition is 0) and not skipIntro
            @currentState @states.INTRO
        else
            @currentState @states.ELEMENTS

    currentState: (state)=>
        if state?
            @scope.state = state
            @userPosition.currentState @scope.state
        @scope.state

    startThematic: =>
        @currentState(@states.ELEMENTS)

    skipElement: (skipped=false) =>
        if skipped and @scope.currentElement.type is "question"
            @Answer.deleteAnswerForQuestion @scope.currentElement.id

        if @hasNextElement()
            @userPosition.nextElement()
        else if @isDone()
            @userPosition.nextThematic()
            (do @userPosition.thematicPosition)
            if (do @userPosition.thematicPosition) < @thematicService.positionList.elements.length
                @currentState @states.LANDING
            else
                @scope.$parent.setState @scope.$parent.survey.states.OUTRO
        else
            @currentState(@states.OUTRO)

    previousElement: =>
        if @isIntro()
            @userPosition.previousThematic()        
            @currentState(@states.ELEMENTS)
        else if @hasPreviousElement()
            @userPosition.previousElement()
        else
            @currentState(@states.INTRO)

    hasNextElement: => 
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() + 1)
        if element then true else false

    hasPreviousElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() - 1)
        if element then true else false

    isLanding : => @currentState() == @states.LANDING
    isIntro   : => @currentState() == @states.INTRO
    isElements: => @currentState() == @states.ELEMENTS
    isDone    : => @isElements() and @userPosition.elementPosition() == @elements.count() - 1

    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        @elements = @userPosition.createWrapper thematic.elements
        @scope.thematicWrapper = @elements

        if (typeof thematic.intro_description) is typeof String
            _.extend @scope.thematic.currentThematic,
                intro_description: @sce.trustAsHtml(thematic.intro_description)
        else
            _.extend @scope.thematic.currentThematic,
                intro_description: thematic.intro_description

        if thematic.position is 1
            @currentState @states.INTRO

        @onElementPositionChanged do @userPosition.elementPosition

    onElementPositionChanged: (position)=>
        return unless @elements?
        @scope.currentElement = @elements.getAt position

angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl