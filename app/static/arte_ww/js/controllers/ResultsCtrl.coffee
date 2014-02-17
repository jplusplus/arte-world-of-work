class ResultsCtrl
    @$inject: [ '$scope']
    constructor: ($scope) ->
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

angular.module('arte-ww') 
.controller('ResultsCtrl', ResultsCtrl)  