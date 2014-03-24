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
                @Thematic.currentThematic
            , @onThematicChanged

        @rootScope.$watch => 
                @userPosition.elementPosition()
            , @onElementPositionChanged

        @rootScope.$watch =>
                @currentElement
            , @onElementChanged

    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        @elements = @userPosition.createWrapper thematic.elements
        @list = @elements
        @onElementPositionChanged do @userPosition.elementPosition

    onElementPositionChanged: (position, old_position)=>
        return unless @elements? and position?
        challenger = @elements.getAt position

        if !@currentElement
            @currentElement = challenger


        # @currentElement need to be updated but we'll check if we should
        # load a feedback for this element or not.
        if position > old_position and @feedbackService.distanceIsGood()
            # check if old element should display a feedback
            promise = @feedbackService.getForQuestion(@currentElement.id)
            promise.then (dynFeedback)=>
                console.log 'received dat feedback: ', dynFeedback
                if dynFeedback.hasEnoughAnswers()
                    feedback = dynFeedback
                else if challenger.feedback
                    feedback = @utils.wrapFeedback challenger.feedback
                
                if @shouldDisplayFeedback()
                    @elements.insertAt position, feedback
                else
                    if !challenger
                        @userPosition.nextThematic()

                @currentElement = @elements.getAt position
        else
            @currentElement = @elements.getAt position

    onElementChanged: (new_el, old_el)=>
        if new_el and new_el.type is 'feedback'
            @feedbackService.resetDistance()
        else if old_el and new_el.position > old_el.position
            @feedbackService.increaseDistance()
        else if old_el and new_el.position < old_el.position 
            @feedbackService.decreaseDistance()

    shouldDisplayFeedback: =>
        return false unless @feedbackService.distanceIsGood()
        return false unless @Thematic.currentThematic.slug != 'toi'
        # return Math.floor(Math.random()*5)+1 == 1
        return true # Math.floor(Math.random()*5)+1 == 1

    hasNextElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() + 1)
        if element then true else false

    hasPreviousElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() - 1)
        if element then true else false

    # wrapped .count method
    count: => @allQuestions().length

    all: => if @elements then @elements.all() else []  

    allQuestions: => _.filter(@all(), question_only )

    getAt: (pos)=> @elements.getAt pos

angular.module('arte-ww.services').service 'ElementsWrapper', ElementsWrapper