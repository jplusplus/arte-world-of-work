class PositionsObject
    constructor: (elements, @utils)->
        @elements = _.map @elements, @wrapElem
        @elements = _.sortBy elements, (el)-> el.position
        do @updateIDS
        do @updatePositions

    updatePositions: =>
        @positions =  _.map(@elements, (el)-> el.position )

    updateIDS: =>
        @elements = _.map @elements, (el,i)->
            el = _.extend el, _id: i
            if not el.id
                el.id = el._id 
            el

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
        @elements  = _.union left_part, [el], right_part
        @updateIDS()
        @updatePositions()

    count: => @elements.length

    wrapElem: (el)=>
        return unless el.type 
        if el.type is 'question'
            el = @utils.wrapQuestion(el)
        else if el.type is 'feedback'
            el = @utils.wrapFeedback(el)

class UserPositionService
    @$inject: ['$http', 'utils']

    state: undefined
    positions:
        thematicPosition: undefined
        elementPosition: undefined

    constructor: (@$http, @utils) ->
        @utils.authenticate (=>
            request =
                url : '/api/my-position'
                method : 'GET'
            ((@$http request).success (data) =>
                @positions =
                    thematicPosition : data.thematic_position
                    elementPosition : data.element_position
            ).error =>
                @positions =
                    thematicPosition : 0
                    elementPosition : 0
        ), no

    currentState: (state) =>
        if state?
            @state = state
        @state

    sendPosition: =>
        request =
            url : '/api/my-position/'
            method : 'PATCH'
            data :
                thematic_position : @positions.thematicPosition
                element_position : @positions.elementPosition
        @$http request

    thematicPosition: (position) =>
        if position?
            @positions.thematicPosition = position
            do @sendPosition
        @positions.thematicPosition

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

    nextElement: =>
        @elementPosition @positions.elementPosition + 1

    previousElement: =>
        @elementPosition @positions.elementPosition - 1

    createWrapper: (elements)-> return new PositionsObject(elements, @utils)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService