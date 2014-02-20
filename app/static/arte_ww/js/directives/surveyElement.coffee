angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "AE"
            replace: yes
            templateUrl: "partial/directives/survey-element.html"
            link: (scope, elem, attrs)->
                scope.$watch -> 
                        scope.$eval(attrs.surveyElement)
                    , (element)->
                        scope.element = element

]