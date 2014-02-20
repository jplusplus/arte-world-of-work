class Utils
    # -------------------------------------------------------------------------
    # Utility service for front-end application
    #
    # attributes:
    #    - states: common state name / value shared accross components
    # -------------------------------------------------------------------------
    states: 
        survey:
            INTRO: 0
            DOING: 1
            OUTRO: 2
        thematic: 
            INTRO: 0
            ELEMENTS: 1
            OUTRO: 2

angular.module('arte-ww.utils').service('utils', Utils)