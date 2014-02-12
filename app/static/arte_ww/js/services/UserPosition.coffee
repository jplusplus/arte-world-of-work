# TODO: handle user position saving and loading/intialization
class UserPositionService
    @$inject: ['$rootScope']

    constructor: ($rootScope)->
        @thematicPosition = 0
        @elementPosition  = 0

    nextThematic: =>
        @thematicPosition+=1

    previousThematic: =>
        @thematicPosition-=1

    nextElement: =>
        @elementPosition+=1

    previousElement: => 
        @elementPosition-=1


angular.module('arte-ww.services').service 'UserPosition', UserPositionService