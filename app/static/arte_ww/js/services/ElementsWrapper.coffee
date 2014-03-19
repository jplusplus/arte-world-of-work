# Top responsibilties:
# - handle what element should be shown based on user's position. 
# - handle dynamic feedback loading
class ElementsWrapper
    @$inject: [
        '$rootScope', 'utils' , 'UserPosition', 'Thematic', 'Feedback'
    ]
    constructor: (@rootScope, @utils , @userPosition, @Thematic, @feedbackService)->
        # ---------------------------------------------------------------------
        # watches 
        # ---------------------------------------------------------------------
        @rootScope.$watch =>
                @Thematic.currentThematic
            , @onThematicChanged
        @rootScope.$watch => 
                @userPosition.elementPosition()
            , @onElementPositionChanged

    onThematicChanged: (thematic, old_thematic)=>
        return unless thematic?
        @elements = @userPosition.createWrapper thematic.elements
        @list = @elements
        @onElementPositionChanged do @userPosition.elementPosition

    onElementPositionChanged: (position, old_position)=>
        return unless @elements?
        @currentElement = @elements.getAt position
        if do @hasNextElement
            next_element = @elements.getAt position + 1 
        
        @checkFeedbackFor next_element, position + 1 
        if @currentElement.type is 'feedback'
            @feedbackService.resetDistance()
        else
            if position > old_position or !old_position?
                @feedbackService.increaseDistance()
            else if position < old_position
                @feedbackService.decreaseDistance()

    hasNextElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() + 1)
        if element then true else false

    hasPreviousElement: =>
        return false unless @elements
        element = @elements.getAt(@userPosition.elementPosition() - 1)
        if element then true else false

    # wrapped .count method
    count: => @elements.count() 

    checkFeedbackFor: (element, position)=>
        return unless element
        return if element.type is 'feedback'
        console.log 'checkFeedbackFor'
        next_element = @elements.getAt position + 1
        if (next_element and next_element.type != 'feedback') or (!next_element?)
            if @feedbackService.isDistanceFarEnought()
                @feedbackService.getForQuestion(element.id).then (dynFeedback)=>
                    console.log 'received feedback: ', dynFeedback
                    if dynFeedback.hasEnoughAnswers()
                        console.log('if dynFeedback.hasEnoughAnswers()')
                        feedback = dynFeedback
                    else if element.feedback
                        console.log('else if element.feedback')
                        feedback = element.feedback
                    if feedback
                        console.log 'feedback for element (',element,'):', feedback
                        @elements.insertAt position + 1, feedback




angular.module('arte-ww.services').service 'ElementsWrapper', ElementsWrapper