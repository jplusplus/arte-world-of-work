angular.module('arte-ww').directive 'questionUserGender', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-user-gender.html"
            link: (scope, elem, attrs)->
                scope.question = scope.$parent.element
                scope.$watch '$parent.element', -> scope.question = scope.$parent.element               
                
]
