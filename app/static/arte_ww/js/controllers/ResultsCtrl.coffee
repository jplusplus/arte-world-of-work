class ResultsCtrl
    @$inject: [ '$scope']
    constructor: ($scope) ->
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

        $scope.filters =
            age_min : 0
            age_max : 99
            male : yes
            female : yes

angular.module('arte-ww') 
.controller('ResultsCtrl', ResultsCtrl)  