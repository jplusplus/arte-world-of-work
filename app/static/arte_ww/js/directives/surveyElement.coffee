angular.module('arte-ww').directive 'surveyElement', [
    ()->
        directive = 
            restrict: "AE"
            scope:
                ngModel: "=" 

            link: (scope, elem, attr)->
                
                console.log elem, scope, attr

]