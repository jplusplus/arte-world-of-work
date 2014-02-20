class PositionsObject
    constructor: (elements)->
        @elements  =  _.sortBy elements, (el)-> el.position
        @positions =  _.map(@elements, (el)-> el.position )

    positionAt: (i)=> @positions[i]

    getAt: (i)=> _.findWhere @elements, position: @positionAt(i)

    count: => @elements.length 


# TODO: handle user position saving and loading/intialization
class UserPositionService
    positions:
        thematicPosition: 0
        elementPosition: 0

    thematicPosition: (position)=> 
        if position?
            @positions.thematicPosition = position
        @positions.thematicPosition

    elementPosition:  (position)=> 
        if position?
            @positions.elementPosition = position
        @positions.elementPosition

    nextThematic: =>
        @positions.thematicPosition += 1

    previousThematic: =>
        @positions.thematicPosition -= 1

    nextElement: =>
        @positions.elementPosition += 1

    previousElement: => 
        @positions.elementPosition -= 1

    createWrapper: (elements)-> return new PositionsObject(elements)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService