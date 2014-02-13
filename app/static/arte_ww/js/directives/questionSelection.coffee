angular.module('arte-ww').directive 'questionSelection', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-selection.html"
            link: (scope, elem, attrs)->
                scope.answer = 
                    choices: []

                scope.question = scope.$parent.element

                scope.addChoice = _addChoice
                scope.removeChoice = _removeChoice

                _addChoice = (choice)->
                    console.log '_addChoice'
                    $scope.answer.choices.append choice

                _removeChoice = (choice)->
                    console.log '_removeChoice'
                    $scope.answer.choices = _.reject($scope.answer.choices, (el)-> el.id == choice.id)


                

]
