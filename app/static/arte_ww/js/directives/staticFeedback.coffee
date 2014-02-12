angular.module('arte-ww').directive 'staticFeedback', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/static-feedback.html"
            scope:
                element: "=" 
]
