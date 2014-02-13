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
        @thematicPosition(@thematicPosition()+1)

    previousThematic: =>
        @thematicPosition(@thematicPosition()-1)

    nextElement: =>
        @elementPosition(@elementPosition()+1)

    previousElement: => 
        @elementPosition(@elementPosition()-1)


angular.module('arte-ww.services').service 'UserPosition', UserPositionService