### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$scope', 'utils',  'UserPosition', 'Thematic']

    constructor: (@scope, @utils, @userPosition, @thematicService)->
        # ---------------------------------------------------------------------
        # Class attributes
        # ---------------------------------------------------------------------
        @states = utils.states.thematic
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.thematic = 
            state: @states.INTRO
            states: @states

        @scope.positions = @userPosition.positions

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        @scope.previousElement =  @previousElement
        @scope.skipElement =  @skipElement

        # ---------------------------------------------------------------------
        # Watches 
        # ---------------------------------------------------------------------
        @scope.$watch ()=>
                @userPosition.thematicPosition()
            , @onThematicPositionChanged

        @scope.$watch 'currentThematic', @onThematicChanged

    currentThematic: => @scope.currentThematic

    currentState: (state)=> 
        if state?
            @scope.thematic.state = state
        return @scope.thematic.state

    skipElement: =>
        if @hasNextElement()
            @userPosition.nextElement()
        else if @isOutro()
            @userPosition.nextThematic()
        else
            @currentState(@states.OUTRO)

    previousElement: =>
        if @isIntro()
            @userPosition.previousThematic()
        else if @isOutro()
            @currentState(@states.ELEMENTS)
        else if @hasPreviousElement()
            @userPosition.previousElement()
        else
            @currentState(@states.INTRO)

    hasNextElement: => 
        thematic = @currentThematic()
        return false unless thematic
        thematic.elements[@userPosition.elementPosition() + 1]?

    hasPreviousElement: =>
        thematic = @currentThematic()
        return false unless thematic
        thematic.elements[@userPosition.elementPosition() - 1]?

    isIntro: => @currentState() == @states.INTRO

    isOutro: => @currentState() == @states.OUTRO

    onThematicPositionChanged: (position)=>
        @thematicService.getAt position-1, (thematic)=>
            @scope.currentThematic = thematic

    onThematicChanged: (thematic, old_thematic)=>
        shouldSetOutro = old_thematic? and thematic.position > old_thematic.position
        @currentState(if shouldSetOutro then @states.OUTRO else @states.INTRO)
        if @isIntro()
            elementPosition = 1 
        else 
            elementPosition = thematic.elements.length - 1 if thematic.elements

        @userPosition.elementPosition(elementPosition)

angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl