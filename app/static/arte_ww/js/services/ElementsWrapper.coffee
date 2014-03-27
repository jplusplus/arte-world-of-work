# Top responsibilties:
# - handle what element should be shown based on user's position. 
# - handle dynamic feedback loading
question_only = (el)-> el.type and el.type is 'question'

class ElementsWrapper
    @$inject: [
        '$rootScope', 'utils' , 'UserPosition', 'Thematic', 'Answer', 'Feedback'
    ]
    constructor: (@rootScope, @utils , @userPosition, @Thematic, @Answer, @feedbackService)->
        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @rootScope.$watch =>
                @userPosition.thematicPosition()
            , @onThematicChanged, yes

        @rootScope.$watch => 
                @userPosition.elementPosition()
            , @onElementPositionChanged, yes

        @rootScope.$watch =>
                @currentElement
            , @onElementChanged

    onThematicChanged: (thematicposition, old_thematicposition)=>
        if thematicposition?
            @Thematic.getAt thematicposition, ((o) =>
                return (thematic) =>
                    return unless thematic?
                    @elements = @userPosition.createWrapper thematic.elements
                    @onElementPositionChanged do @userPosition.elementPosition
            ) @

    onElementPositionChanged: (position, old_position)=>
        return unless @elements? and position?
        challenger = @getAt position
        # first time we arrive on the widget 
        if !@currentElement and challenger
            console.log 'onElementPositionChanged if !@currentElement and challenger'
            @currentElement = challenger

        # we initialized the widget with a wrong position 
        if !challenger and !old_position 
            console.log 'onElementPositionChanged if !challenger and !old_position'
            @fixPosition(position)

        # load a feedback for this element or not.
        # if position > old_position and @feedback.distanceIsGood()
        if position > old_position and @shouldDisplayFeedback()
            console.log 'we should display feedback for current element'
            # check if old element should display a feedback
            promise = @feedbackService.getForQuestion(@currentElement.id)
            promise.then (dynFeedback)=>
                console.log dynFeedback, dynFeedback.total_answers
                if dynFeedback.total_answers >= 10
                    feedback = dynFeedback
                else if @currentElement.feedback
                    feedback = @utils.wrapFeedback @currentElement.feedback
                feedback.question = @currentElement
                # if @shouldDisplayFeedback() and feedback
                if feedback
                    @elements.insertAt position, feedback

                challenger = @elements.getAt position
                @currentElement = challenger
        else
            @currentElement = challenger

    fixPosition: (position)=>
        # console.log 'fixPosition(', position, ')'
        nb_elem = @all().length
        if position >= nb_elem
            @userPosition.elementPosition(nb_elem - 1)
            @onElementPositionChanged do @userPosition.elementPosition
            # @rootScope.$apply()

    onElementChanged: (new_el, old_el)=>
        return unless new_el
        if new_el and new_el.type is 'feedback'
            @feedbackService.resetDistance()
        else if !old_el and new_el
            @feedbackService.increaseDistance()
        else if old_el and new_el
            if new_el.position > old_el.position
                @feedbackService.increaseDistance()
            else 
                @feedbackService.decreaseDistance()

    shouldDisplayFeedback: =>
        # return false unless @feedbackService.distanceIsGood()
        return false if @isYou()
        return false if @currentElement.type is 'feedback'
        # return Math.floor(Math.random()*5)+1 == 1
        return true

    hasNextElement: =>
        return false unless @elements
        position = @userPosition.elementPosition()
        element = @elements.getAt( position + 1)
        if position <= @all().length and !@isYou()
            result = true
        else
            result = if element then true else false
        result

    hasPreviousElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() - 1)
        if element then true else false

    # wrapped .count method
    count: => @allQuestions().length

    all: => if @elements then @elements.all() else []  

    allQuestions: => _.filter(@all(), question_only )

    getAt: (pos)=> @elements.getAt pos

    isYou: => @Thematic.currentThematic.slug == 'toi'

angular.module('arte-ww.services').service 'ElementsWrapper', ElementsWrapper