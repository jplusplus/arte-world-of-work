angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "AE"
            templateUrl: "partial/directives/survey-element.html"
            compile: ->
                    pre: (scope, elem, attrs)->
                        scope.element = scope.$eval(attrs.surveyElement)

]