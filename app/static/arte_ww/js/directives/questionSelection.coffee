angular.module('arte-ww').directive 'questionSelection', [
    ()->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/question-selection.html"
            link: (scope, elem, attrs)->
                scope.answer =  [] unless angular.isArray(scope.answer)
                _isSelected = (choice)->
                    return choice.id in scope.answer 

                _toggleChoice = (choice)->
                    if _isSelected(choice)
                        scope.answer = _.without(scope.answer, choice.id)
                    else
                        scope.answer.push choice.id
                    
                # -------------------------------------------------------------
                # Scope variables binding 
                # -------------------------------------------------------------
                scope.question = scope.$parent.element

                # -------------------------------------------------------------
                # Scope functions binding 
                # -------------------------------------------------------------
                scope.isSelected   = _isSelected
                scope.toggleChoice = _toggleChoice
]
