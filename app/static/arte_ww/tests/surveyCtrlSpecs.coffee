describe 'arte-ww.ThematicCtrl', ->
    ctrl = scope = null 

    # load main module
    beforeEach module('arte-ww')

    beforeEach(inject(
        ($injector, $rootScope, $controller)->
            scope = $rootScope.$new()
            ctrl =  $controller('ThematicCtrl', {$scope: scope })
    ))

    it 'should have initialized scope variables', ->
        # currentPosition should be 0 
        expect(ctrl.scope.thematic.state).toBe 0



            
