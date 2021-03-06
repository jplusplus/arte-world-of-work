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

    constructor: ( @scope, @sce, @utils, @userPosition, @thematicService, @Answer, @feedbackService, @elementsWrapper)->
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
            elements: => @elements()
            currentElement: => @currentElement

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
        @scope.$watch => 
                @elementsWrapper.currentElement
            , @onElementChanged

    letsgo: (skipIntro=false) =>
        if (do @userPosition.elementPosition is 0) and not skipIntro
            @currentState @states.INTRO
        else
            @currentState @states.ELEMENTS

    elements: => @elementsWrapper.all()

    currentState: (state)=>
        if state?
            @scope.state = state
            @userPosition.currentState @scope.state
        @scope.state

    startThematic: =>        
        @currentState(@states.ELEMENTS)

    skipElement: (skipped=false) =>
        if skipped
            @Answer.deleteAnswerForQuestion @currentElement.id
        
        if @elementsWrapper.hasNextElement()
            @userPosition.nextElement()
        else if @isDone()
            @setNextThematic()
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
    isDone    : => @isElements() and @userPosition.elementPosition() >= @elements().length - 1

    setNextThematic: =>
        @userPosition.nextThematic()
        (do @userPosition.thematicPosition)
        if (do @userPosition.thematicPosition) < @thematicService.count()
            @currentState @states.LANDING
        else
            @scope.$parent.setState @utils.states.survey.OUTRO

    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        if (typeof thematic.intro_description) is typeof String
            _.extend @scope.thematic.currentThematic,
                intro_description: @sce.trustAsHtml(thematic.intro_description)
        
        # special case for "You" thematic to skip the landing page. 
        # !! DO NOT CHANGE !!
        if @userPosition.thematicPosition() is 0
            do @letsgo


    onElementChanged: (elem, old_elem)=>
        elem_pos = @userPosition.elementPosition()
        out_of_range = elem_pos >= @elements().length 
        # # security check, to pass to next thematic if last element is undefined
        # # this undefined value can occur if we wanted to show a feedback for the 
        # # last element of the current thematic
        if old_elem and !elem and @isDone()
            @setNextThematic()

        if elem?
            @currentElement = elem
        # if elem and !@isElements() and !@isIntro()
        #     @currentState @states.ELEMENTS



angular.module('arte-ww').controller 'ThematicCtrl', ThematicCtrl