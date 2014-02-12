angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "AE"
            templateUrl: "partial/directives/survey-element.html"
            link: (scope, elem, attrs)->
                scope.element = scope.$eval(attrs.surveyElement)

]