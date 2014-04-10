# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:05
# Last Modified time: 2014-04-10 12:13:15
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.


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

    





