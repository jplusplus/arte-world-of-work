angular.module('arte-ww').directive 'questionBoolean', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-boolean.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
                scope.$watch '$parent.element', -> scope.question = scope.$parent.element               
                
]


