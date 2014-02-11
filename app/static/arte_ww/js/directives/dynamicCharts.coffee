class Chart
    constructor: (@scope, @element) ->
        @svg = (d3.select @element[0]).append 'svg'
        @svg.attr
            width: do @element.width
            height: (do @element.width) * 0.8

class PieChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

angular.module('arte-ww').directive 'dynamicChart', [->
    directive =
        template: '<div></div>'
        replace: yes
        restrict: 'E'
        scope:
            data: '='
        link: (scope, elem, attr) ->
            scope.chart = undefined
            switch scope.data.chart_type
                when 'pie' then scope.chart = new PieChart scope, elem
                else throw "Chart type '#{scope.data.chart_type}' does not exist."
]