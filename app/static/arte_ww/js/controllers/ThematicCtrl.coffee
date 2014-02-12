### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$scope',  'UserPosition', 'Thematic']

    constructor: (@scope, @userPosition, @thematicService)->
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        
        @scope.thematic = 
            state: 0
        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            previous: @previousElement
            skip: @skipElement

        # Watches 
        @scope.$watch =>
                @userPosition.thematicPosition
            , @onThematicChanged 

        @scope.$watch =>
                @userPosition.elementPosition
            , @onElementChanged



    skipElement: =>
        @userPosition.nextElement()

    previousElement: =>
        if @userPosition.elementPosition is 0
            @scope.thematic.state = 0
        else
            @userPosition.previousElement()

    isIntro: => return @scope.survey.thematic.state == 0

    isOutro: => return @scope.survey.thematic.state == 2


    onThematicChanged: (new_position, old_position)=> 
        @thematicService.getAt new_position, (thematic)=>
            @scope.currentThematic = thematic
            @scope.currentElement = thematic.elements[0]


    onElementChanged: (position)=>
        return unless @scope.currentThematic
        @scope.currentElement = @scope.currentThematic.elements[position]

angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl