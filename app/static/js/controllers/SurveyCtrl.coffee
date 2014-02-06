class SurveyCtrl
    @$inject: [ '$scope', 'Survey', 'utils']

    constructor: (@scope, @Survey, @utils)->

        Survey.get {}, (l)=>
            @thematics = l

        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.currentThematicPosition = 0
        @scope.currentElementPosition = 0

        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, { skip: @skip, previous: @previous } 
        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @scope.$watch 'currentElementPosition',  @onCurrentPositionChanged
        @scope.$watch 'currentThematicPosition', @onCurrentThematicPositionChanged

    skip: => 
        @scope.currentPosition += 1

    previous: =>
        @scope.currentPosition -= 1

    hasNextElement: => do @hasNextThematic or @hasNextThematicElement

    onCurrentPositionChanged: =>
        if @scope.currentPosition > @scope.currentThematic.elements.length + 2
            @scope.currentThematicPosition += 1 if do @hasNextThematic
        else if @scope.currentPosition < 0
            @scope.currentThematicPosition -= 1 if do @hasPreviousThematic
        else
            @scope.currentElement = @getElement(current_position)

    onCurrentThematicPositionChanged: (old_pos, new_pos)=>
        @scope.currentThematic = @thematics[@scope.currentThematicPosition]
        if old_pos > new_pos
            w


    hasPreviousThematic: => @thematics[@scope.currentThematic - 1]?
    hasNextThematic: => @thematics[@scope.currentThematic + 1]?

    hasNextThematicElement: => 
        position = @scope.currentPosition
        elements = @scope.currentThematic.elements
        elements.length == (position + 1) or elements[position + 1]?

angular.module('arte-ww') 
    .controller('SurveyCtrl', SurveyCtrl) 