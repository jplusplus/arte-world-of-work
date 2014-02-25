### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$rootScope', '$scope', 'utils', 'UserPosition', 'Thematic' ]

    constructor: (@rootScope, @scope, @utils, @userPosition, @thematicService)->
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

        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @scope.$watch 'thematic.currentThematic', @onThematicChanged 
        @scope.$watch => 
                @userPosition.elementPosition()
            , @onElementPositionChanged

    currentState: (state)=>
        if state?
            @scope.state = state
            @userPosition.currentState @scope.state
        @scope.state

    startThematic: =>
        @currentState(@states.ELEMENTS)

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
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() + 1)
        if element then true else false

    hasPreviousElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() - 1)
        if element then true else false

    isLanding: => @currentState() == @states.LANDING
    isIntro  : => @currentState() == @states.INTRO
    isOutro  : => @currentState() == @states.OUTRO
  
    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        @elements = @userPosition.createWrapper thematic.elements
        shouldSetOutro = old_thematic? and thematic.position < old_thematic.position

        @currentState(if shouldSetOutro then @states.OUTRO else @states.LANDING)
        if @isIntro() or @isLanding()
            elementPosition = 0
        else
            elementPosition = @elements.count() - 1
        @userPosition.elementPosition(elementPosition)

    onElementPositionChanged: (position)=>
        return unless @elements?
        @scope.currentElement = @elements.getAt position

angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl