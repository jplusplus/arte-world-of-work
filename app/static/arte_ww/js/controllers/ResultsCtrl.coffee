class ResultsCtrl
    @$inject: [ '$scope']
    constructor: ($scope) ->
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

        # Some fake data
        $scope.piedata = {
            "question": { },
            "sets": {
                1 : { name : 'yes' },
                2 : { name : 'no' }
            },
            "chart_type": "pie",
            "results": {
                1 : 1435,
                2 : 656
            },
            "total_answers": 2000
        };
        $scope.hbardata = {
            "question": { },
            "sets": {
                1 : { name : 'Un DVD' },
                2 : { name : 'Un iPad' },
                3 : { name : 'Le fixie du patron' }
            },
            "chart_type": "hbar",
            "results": {
                1 : 535,
                2 : 841,
                3 : 624
            },
            "total_answers": 2000
        };
        $scope.histodata = {
            "question": { },
            "sets": {
                1 : { min : 0, max : 400 },
                2 : { min : 400, max : 800 },
                3 : { min : 800, max : 1200 },
                4 : { min : 1200, max : 1600 },
                5 : { min : 1600, max : 2000 }
            },
            "chart_type": "histo",
            "results": {
                1 : 840,
                2 : 513,
                3 : 1656,
                4 : 213,
                5 : 126
            },
            "total_answers": 2000
        };

angular.module('arte-ww') 
.controller('ResultsCtrl', ResultsCtrl)  