angular.module('arte-ww').directive 'feedbackStatic', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/feedback-static.html"
            compile: ->
                pre: (scope, elem, attrs)->
                    scope.feedback = scope.$parent.scope

]
