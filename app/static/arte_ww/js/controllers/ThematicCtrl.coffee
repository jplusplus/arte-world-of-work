# TODO
# -> handle skip when on feedback
# -> handle previous on feedback 

### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [
        '$scope'
        '$sce'
        'utils'
        'UserPosition'
        'Thematic'
        'Answer'
        'Feedback'
        'ElementsWrapper'
    ]

    constructor: ( @scope, @sce, @utils, @userPosition, @thematicService, @Answer, @feedbackService, @elementsWrapper )->
        @scope.$watch (=>
            @userPosition.positions
        ), (newdata, olddata) =>
            if newdata.elementPosition? and newdata.thematicPosition? and @scope.state is @states.LANDING
                if newdata.thematicPosition is olddata.thematicPosition
                    if (newdata.elementPosition isnt 0) or newdata.thematicPosition isnt 0
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
            # function binding
            elements: @elements
            currentElement: @currentElement

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

        # watches
        @scope.$watch 'thematic.currentThematic', @onThematicChanged 

    letsgo: (skipIntro=false) =>
        if (do @userPosition.elementPosition is 0) and not skipIntro
            @currentState @states.INTRO
        else
            @currentState @states.ELEMENTS

    elements: => @elementsWrapper.all()

    currentElement: => @elementsWrapper.currentElement

    currentState: (state)=>
        if state?
            @scope.state = state
            @userPosition.currentState @scope.state
        @scope.state

    startThematic: =>
        @currentState(@states.ELEMENTS)

    skipElement: (skipped=false) =>
        if skipped
            # console.log "if skipped"
            @Answer.deleteAnswerForQuestion @scope.currentElement().id
        else if @elementsWrapper.hasNextElement()
            # console.log "else if @elementsWrapper.hasNextElement()"
            @userPosition.nextElement()
        else if @isDone()
            # console.log "else if @isDone()"
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
        else if @elementsWrapper.hasPreviousElement()
            @userPosition.previousElement()
        else
            @currentState(@states.INTRO)

    isLanding : => @currentState() == @states.LANDING
    isIntro   : => @currentState() == @states.INTRO
    isElements: => @currentState() == @states.ELEMENTS

    isDone    : => 
        pos = @userPosition.elementPosition()
        return false unless @isElements()
        is_last_element = pos == @elementsWrapper.count() - 1
        last_elem = @elementsWrapper.getAt pos
        if last_elem and last_elem.type is 'question'
            if @elementsWrapper.shouldDisplayFeedback()
                return false 
            else
                return true
        else
            return is_last_element

    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        if (typeof thematic.intro_description) is typeof String
            _.extend @scope.thematic.currentThematic,
                intro_description: @sce.trustAsHtml(thematic.intro_description)
        else
            _.extend @scope.thematic.currentThematic,
                intro_description: thematic.intro_description

        if thematic.position is 1
            @currentState @states.INTRO

angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl