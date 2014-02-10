### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$scope', 'Thematic', 'utils']

    constructor: (@scope, @Thematic, @utils)->

        @scope.thematic = 
            state: 0
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.currentThematicPosition = 0
        @scope.currentElementPosition = 0

        @Thematic.all (l)=>
            @thematics = l
            @scope.currentThematic = @thematics[@scope.currentThematicPosition]

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, { skip: @skip, previous: @previous, isIntro: @isIntro } 
        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @scope.$watch 'currentElementPosition',  @onCurrentPositionChanged
        @scope.$watch 'currentThematicPosition', @onCurrentThematicPositionChanged

    skip: =>
        @scope.currentElementPosition += 1

    previous: =>
        @scope.currentElementPosition -= 1

    hasNextElement: => do @hasNextThematic or @hasNextThematicElement

    onCurrentPositionChanged: =>
        return unless @scope.currentThematic

        if @scope.currentPosition > @scope.currentThematic.elements.length + 2
            @scope.currentThematicPosition += 1 if do @hasNextThematic
        else if @scope.currentPosition < 0
            @scope.currentThematicPosition -= 1 if do @hasPreviousThematic
        else
            @scope.currentElement = @getElement(current_position)

    isIntro: => @scope.currentElementPosition is 0

    hasPreviousThematic: => @thematics and @thematics[@scope.currentThematic - 1]?
    hasNextThematic: => @thematics and @thematics[@scope.currentThematic + 1]?

    hasNextThematicElement: => 
        position = @scope.currentPosition
        elements = @scope.currentThematic.elements
        elements.length == (position + 1) or elements[position + 1]?

angular.module('arte-ww') 
    .controller('ThematicCtrl', ThematicCtrl) 