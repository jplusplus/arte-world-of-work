class PositionsObject
    constructor: (elements, @utils)->
        elements = @wrapElements(elements)
        @updateElements(elements)

    get_pos = (el)-> 
        return el unless el
        el.position

    set_index_as_pos = (el,i)-> 
        return el unless el
        el.position = i
        el

    makeElementPositionsUnique:(elements)=>
        elements  = _.sortBy elements, get_pos
        elements  = _.map    elements, set_index_as_pos
        elements

    updateElements: (elements)=>
        elements  = elements or @elements
        elements  = @makeElementPositionsUnique(elements)
        elements  = @updatePositions(elements)
        @elements = elements


    updatePositions:(elements)=>
        @positions =  _.map(elements, get_pos)
        elements

    positionAt: (i)=> @positions[i]

    getAt: (i)=> _.findWhere @elements, position: @positionAt(i)

    insertAt: (i, el)=>
        left_part   = _.first( @elements, i )
        right_part  = _.rest(  @elements, i )
        if left_part.length > 0
            el.position = _.last( left_part ).position + 1
        else
            el.position = _.first( right_part ).position
        _.each right_part, (el)-> el.position += 1
        elements  = _.union left_part, [el], right_part
        @updateElements(elements)

    count: => @elements.length

    wrapElem: (el)=>
        return el unless el.type?
        if el.type is 'question'
            el = @utils.wrapQuestion(el)
        else if el.type is 'feedback'
            el = @utils.wrapFeedback(el)
        el

    wrapElements: (elements)=> _.map elements, @wrapElem

    all: => @elements

class UserPositionService
    @$inject: ['$rootScope', '$http', 'utils']

    state: undefined
    positions:
        lastElementPosition: undefined
        thematicPosition: undefined
        elementPosition: undefined

    constructor: (@rootScope, @$http, @utils) ->
        # Notify rootScope to display a loading spinner
        @rootScope.isUserLoading = yes 

        @utils.authenticate (=>
            request =
                url : '/api/my-position'
                method : 'GET'
            ((@$http request).success (data) =>
                # Disabled loading spinner
                @rootScope.isUserLoading = no
                
                @positions =
                    thematicPosition : data.thematic_position
                    elementPosition : data.element_position
            ).error =>
                # Disabled loading spinner  
                @rootScope.isUserLoading = no

                @positions =
                    thematicPosition : 0
                    elementPosition : 0
        ), no

    currentState: (state) =>
        if state?
            @state = state
        @state

    sendPosition: () =>
        request =
            url : '/api/my-position/'
            method : 'PATCH'
            data :
                thematic_position : @positions.thematicPosition
                element_position : @positions.lastElementPosition
        @$http request

    thematicPosition: (position) =>
        if position?
            @positions.thematicPosition = position
            do @sendPosition
        @positions.thematicPosition

    lastElementPosition: (position)=>
        if position?
            @positions.lastElementPosition = position
            do @sendPosition
        @positions.lastElementPosition

    elementPosition:  (position, save=true) =>
        if position?
            @positions.elementPosition = position
            if save
                do @sendPosition
        @positions.elementPosition

    nextThematic: =>
        @currentState( @utils.states.thematic.LANDING )
        @elementPosition 0, false
        @thematicPosition @positions.thematicPosition + 1

    previousThematic: =>
        @currentState( @utils.states.thematic.ELEMENTS )
        @thematicPosition @positions.thematicPosition - 1

    nextElement: (save = true) =>
        @elementPosition @positions.elementPosition + 1, false

    previousElement: (save = true) =>
        @elementPosition @positions.elementPosition - 1, false

    createWrapper: (elements)-> return new PositionsObject(elements, @utils)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService