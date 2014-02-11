class Chart
    constructor: (@scope, @element) ->
        @size =
            width: do @element.width
            height: (do @element.width) * 0.5

        # Create the svg element
        @svg = (d3.select @element[0]).append 'svg'
        @svg.attr
            width: @size.width
            height: @size.height

        # Create a color range
        @color = (do d3.scale.category20)

        @layout = undefined


class PieChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

        # Compute the result into something usable by the pie layout
        @results = []
        _.forEach (_.keys @scope.data.results), (key) =>
            @results.push [key, @scope.data.results[key]]

        # Create arcs
        radius = (Math.min @size.width, @size.height) / 2
        arc = do d3.svg.arc
        arc.outerRadius radius - 100
        arc.innerRadius 0

        # Center the pie
        @svg = (@svg.append 'g').attr 'transform', "translate(#{@size.width / 2}, #{@size.height / 2})"

        # Create the layout
        @layout = do d3.layout.pie
        @layout.value (d) -> d[1]

        # Get all entering data
        g = (do ((@svg.selectAll '.arc').data (@layout @results)).enter).append 'g'
        g.attr '.arc'

        # Append the path
        ((g.append 'path').attr 'd', arc).style 'fill', (d) => @color d.data[0]

        # And append the text
        (g.append 'text')
            .attr
                transform : (d) -> "translate(#{arc.centroid d})"
            .style
                'text-anchor' : 'middle'
            .text (d) -> d.data[0]



angular.module('arte-ww').directive 'dynamicChart', [->
    directive =
        template: '<div></div>'
        replace: yes
        restrict: 'E'
        scope:
            data: '='
        link: (scope, elem, attr) ->
            scope.chart = undefined
            # We instanciate the right chart from data.chart_type
            switch scope.data.chart_type
                when 'pie' then scope.chart = new PieChart scope, elem
                else throw "Chart type '#{scope.data.chart_type}' does not exist."
]