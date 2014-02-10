angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "A"
            scope:
                ngModel: "=" 

            link: (scope, elem, attr)->
                console.log elem, scope, attr

]