# Top responsibilties:
# - handle what element should be shown based on user's position. 
# - handle dynamic feedback loading
question_only = (el)-> el.type and el.type is 'question'

class ElementsWrapper
    @$inject: [
        '$rootScope', 'utils' , 'UserPosition', 'Thematic', 'Answer', 'Feedback'
    ]

    config:
        # set to false to enable dynamic feedbacks too
        onlyStaticFeedback: true
        alwaysShowFeedbacks: true

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
        current    = @currentElement
        next       = @getAt position + 1

        # first time we arrive on the widget 
        if !current and challenger
            current = challenger

        # we initialized the widget with a wrong position 
        if !challenger and !old_position 
            @fixPosition(position)

        # load a feedback for this element or not.
        if position > old_position and @shouldDisplayFeedback() and not @isFeedback(next)
            staticFeedback = current.feedback
            unless @config.onlyStaticFeedback
                # check if old element should display a feedback
                promise = @feedbackService.getForQuestion(current.id)
                promise.then (dynFeedback)=>
                    if @isFeedback(dynFeedback) and dynFeedback.total_answers >= 500
                        feedback = dynFeedback
                        feedback.question = current
                    else if @isFeedback(staticFeedback)
                        feedback = @utils.wrapFeedback staticFeedback
                        feedback.question = current
                    if feedback
                        feedback.question = current
                        @elements.insertAt position, feedback

                    @currentElement = feedback

            else if @isFeedback(staticFeedback)
                staticFeedback.question = @currentElement
                @elements.insertAt position, staticFeedback
            @currentElement = staticFeedback
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
        return true  if @config.alwaysShowFeedbacks
        return Math.floor(Math.random()*3)+1 == 1

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