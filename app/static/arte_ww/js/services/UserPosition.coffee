class PositionsObject
    constructor: (elements)->
        @elements  =  _.sortBy elements, (el)-> el.position
        @positions =  _.map(@elements, (el)-> el.position )

    positionAt: (i)=> @positions[i]

    getAt: (i)=> _.findWhere @elements, position: @positionAt(i)

    count: => @elements.length 


# TODO: handle user position saving and loading/intialization
class UserPositionService
    @$inject: ['$http']

    positions:
        thematicPosition: 0
        elementPosition: 0
    state: undefined

    constructor: (@$http) ->
        request =
            url : '/api/my-position'
            method : 'GET'
        (@$http request).success (data) =>
            console.debug 'get', data
            @positions.thematicPosition = data.thematic_position
            @positions.elementPosition = data.element_position

    currentState: (state) =>
        if state?
            @state = state
        @state

    sendPosition: =>
        request =
            url : '/api/my-position'
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

    elementPosition:  (position) =>
        if position?
            @positions.elementPosition = position
            do @sendPosition
        @positions.elementPosition

    nextThematic: =>
        @thematicPosition @positions.thematicPosition + 1

    previousThematic: =>
        @thematicPosition @positions.thematicPosition - 1

    nextElement: =>
        @elementPosition @positions.elementPosition + 1

    previousElement: =>
        @elementPosition @positions.elementPosition - 1

    createWrapper: (elements)-> return new PositionsObject(elements)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService