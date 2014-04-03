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
                return (thematic)=>
                    return unless thematic?
                    @elements = @userPosition.createWrapper thematic.elements
                    @intitialElements = @elements.all()
                    @onElementPositionChanged do @userPosition.elementPosition
            ) @

    onElementPositionChanged: (position, old_position)=>
        return unless @elements? and position?
        challenger = @getAt position
        # first time we arrive on the widget 
        if !@currentElement and challenger
            @currentElement = challenger

        # we initialized the widget with a wrong position 
        if !challenger and !old_position 
            @fixPosition(position)

        # load a feedback for this element or not.
        # if position > old_position and @feedback.distanceIsGood()
        if position > old_position and @shouldDisplayFeedback()
            staticFeedback = @currentElement.feedback
            # check if old element should display a feedback
            promise = @feedbackService.getForQuestion(@currentElement.id)
            promise.then (dynFeedback)=>
                if @isFeedback(dynFeedback) and dynFeedback.total_answers >= 500
                    feedback = dynFeedback
                else if @isFeedback(staticFeedback)
                    feedback = @utils.wrapFeedback staticFeedback
                if feedback
                    feedback.question = @currentElement
                    @elements.insertAt position, feedback
                @currentElement = @elements.getAt position
        else
            @currentElement = challenger

        [ found, index ] = @isInInitialList(@currentElement)
        if found
            @userPosition.lastElementPosition(index)
        

    fixPosition: (position)=>
        nb_elem = @all().length
        if nb_elem > 0
            if position >= nb_elem
                @userPosition.elementPosition(nb_elem - 1)

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

    isFeedback: (elem)=> elem and elem.type is 'feedback'

    isInInitialList: (elem)=>
        index       = -1 
        return [ false , index ] unless elem 
        
        found_elem  = _.find @intitialElements, (el, i)->
                found = no 
                if el.type is elem.type
                    if el.type is 'question'
                        found = el.label == elem.label
                    else
                        found = el.html_sentence == elem.html_sentence 
                    if found
                        index = i
                return found

        [ found_elem != undefined, index ]

angular.module('arte-ww.services').service 'ElementsWrapper', ElementsWrapper