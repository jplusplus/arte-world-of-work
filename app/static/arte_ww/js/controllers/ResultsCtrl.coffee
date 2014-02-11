class ResultsCtrl
    @$inject: [ '$scope']
    constructor: ($scope) ->
        # $scope.elements = Survey.get(thematic: 1).elements 
        # $scope.currentElements = $scope.elements[0]

        # Some fake data
        $scope.graphdata = {
            "question": { },
            "fields": [
                "yes",
                "no"
            ],
            "chart_type": "pie",
            "results": {
                "yes": 24000,
                "no": 12000
            },
            "total_answers":36000
        };

angular.module('arte-ww') 
.controller('ResultsCtrl', ResultsCtrl)  