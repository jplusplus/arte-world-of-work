### 
Key responsibilities of ThematicCtrl
    - handle different thematic states: thematic introduction
### 
class ThematicCtrl
    @$inject: [ '$scope', 'utils', UserPosition]

    constructor: (@scope, @utils, UserPosition)->
        # ---------------------------------------------------------------------
        # Scope variables bindings
        # ---------------------------------------------------------------------
        @scope.thematic = 
            state: 0
        # ---------------------------------------------------------------------
        # Scope function bindings
        # ---------------------------------------------------------------------
        _.extend @scope, 
            previous: @previousElement
            skip: @skipElement

    skipElement: => 
        UserPosition.skipElement()
        
    previousElement: => 
        UserPosition.previousElement()

angular.module('arte-ww') 
    .controller('ThematicCtrl', ThematicCtrl) 