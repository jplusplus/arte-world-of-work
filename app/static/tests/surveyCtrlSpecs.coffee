
describe 'arte-ww.SurveyCtrl', ->
    ctrl = scope = null 
    # load main module
    beforeEach module('arte-ww')

    beforeEach(inject(
        ($injector, $rootScope, $controller)->
            scope = $rootScope.$new()
            ctrl =  $controller('SurveyCtrl', {$scope: scope})
    ))

    it 'should have initialized scope variables', ->
        # currentPosition should be 0 
        expect(ctrl.scope.currentElementPosition).toBe 0

        # currentThematicPosition should be 0 
        expect(ctrl.scope.currentThematicPosition).toBe 0



            
