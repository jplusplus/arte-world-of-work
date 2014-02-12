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

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            previousElement: @previousElement
            skipElement: @skipElement

        # ---------------------------------------------------------------------
        # Watches 
        # ---------------------------------------------------------------------
         @scope.$watch ()=>
                @userPosition.thematicPosition
            , @onThematicPositionChanged

        @scope.$watch 'currentThematic', @onThematicChanged

        @scope.$watch =>
                @userPosition.elementPosition
            , (position)=> @scope.elementPosition = position

    currentThematic: => @scope.currentThematic

    currentState: (state)=> 
        if state?
            @scope.thematic.state = state
        return @scope.thematic.state

    skipElement: =>
        currentThematic = @currentThematic()
        if @hasNextElement()
            console.log 'ThematicCtrl.skipElement', "if @hasNextElement()"
            @userPosition.nextElement()
        else if @isOutro()
            console.log 'ThematicCtrl.skipElement', "else if @isOutro()"
            @userPosition.nextThematic()
        else
            console.log 'ThematicCtrl.skipElement', "else"
            @scope.thematic.state = @states.OUTRO

    previousElement: =>
        if @isIntro()
            console.log 'ThematicCtrl.previousElement', "if @isIntro()"
            @userPosition.previousThematic()
        else if @hasPreviousElement()
            console.log 'ThematicCtrl.previousElement', "else if @hasPreviousElement()"
            @userPosition.previousElement()
        else
            console.log 'ThematicCtrl.previousElement', "else"
            @scope.thematic.state = @states.INTRO

    hasNextElement: => 
        thematic = @currentThematic()
        return false unless thematic
        elements = thematic.elements
        elements[@userPosition.elementPosition + 1]?

    hasPreviousElement: =>
        thematic = @currentThematic()
        return false unless thematic
        elements = thematic.elements
        elements[@userPosition.elementPosition - 1]?

    isIntro: => @currentState() == @states.INTRO

    isOutro: => @currentState() == @states.OUTRO

    onThematicPositionChanged: (position)=> 
        @thematicService.getAt position, (thematic)=>
            @scope.currentThematic = thematic

    onThematicChanged: (thematic, old_thematic)=>
        shouldSetOutro = old_thematic? and thematic.position > old_thematic.position
        @currentState(if shouldSetOutro then @states.OUTRO else @states.INTRO)
        if @isIntro()
            @userPosition.elementPosition = 0 
        else 
            @userPosition.elementPosition = thematic.elements.length - 1 if thematic.elements


angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl