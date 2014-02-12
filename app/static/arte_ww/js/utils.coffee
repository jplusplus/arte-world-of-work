class Utils
    states: 
        survey:
            INTRO: 0
            DOING: 1
            OUTRO: 2
        thematic: 
            INTRO: 0
            ELEMENTS: 1
            OUTRO: 2
    constructor: ->
        console.log 'Utils.init'


angular.module('arte-ww.utils').service('utils', Utils)