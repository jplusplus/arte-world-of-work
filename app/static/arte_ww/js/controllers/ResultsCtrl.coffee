class ResultsCtrl
    @$inject: [ '$scope']
    constructor: ($scope) ->
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

        # Some fake data
        $scope.graphdata = {
            "question": { },
            "sets": {
                1 : { name : 'yes' },
                2 : { name : 'no' }
            },
            "chart_type": "pie",
            "results": {
                1 : 200,
                2 : 500
            },
            "total_answers": 700
        };

        $scope.testfunc = =>
            $scope.graphdata.results.yes += 1000
            $scope.graphdata.total_answers += 1000

angular.module('arte-ww') 
.controller('ResultsCtrl', ResultsCtrl)  