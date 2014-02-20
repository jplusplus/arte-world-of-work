
describe 'arte-ww.services', ->
    beforeEach ->
        # load main module  
        module('arte-ww')


    describe 'UserPosition service', ->
        userPosition = null
        beforeEach ->
            inject ($injector)->
                userPosition = $injector.get('UserPosition')

        describe 'position wrapper created with createWrapper', ->
            positionList = null
            beforeEach ->
                elements = [
                    { id: 1, position: 1 }
                    { id: 10, position: 10 }
                    { id: 2, position: 2 }
                    { id: 4, position: 4 }
                ]
                positionList = userPosition.createWrapper elements 

            it 'should return the proper positions', ->
                expect( positionList.positionAt 0 ).toBe(1)
                expect( positionList.positionAt 1 ).toBe(2)
                expect( positionList.positionAt 2 ).toBe(4)
                expect( positionList.positionAt 3 ).toBe(10)

            it 'should return the proper elements', ->
                expect( positionList.getAt(0).id).toBe(1)
                expect( positionList.getAt(1).id).toBe(2)
                expect( positionList.getAt(2).id).toBe(4)
                expect( positionList.getAt(3).id).toBe(10)

    





