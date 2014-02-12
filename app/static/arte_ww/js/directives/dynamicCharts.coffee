class Chart
    constructor: (@scope, @element) ->
        # Compute the result into something usable by the pie layout
        @results = []
        _.forEach (_.keys @scope.data.results), (key) =>
            percent = parseInt (@scope.data.results[key] * 100 / @scope.data.total_answers + 0.5)
            @results.push [key, @scope.data.results[key], percent]

        # Create the svg element
        @svg = (d3.select @element[0]).append 'svg'

        # Create a color range
        @color = (do d3.scale.category20)

        @layout = undefined

        do @setSize
        do @update

    setSize: =>
        @size =
            width : do @element.width
            height : do @element.height

        @svg.attr
            width : @size.width
            height : @size.height

    update: =>

class PieChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

    update : =>
        # Create arcs
        radius = (Math.min @size.width, @size.height) / 2
        arc = do d3.svg.arc
        arc.outerRadius radius
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
            .text (d) -> "#{d.data[0]} - #{d.data[2]}%"


class BarChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

    update : =>
        margin =
            top : 20
            right : 10
            bottom : 20
            left : 10
        @_size =
            width : @size.width - margin.right - margin.left
            height : @size.height - margin.top - margin.bottom

        do @defineXY

        @svg = (@svg.append 'g')
            .attr 'transform', "translate(#{margin.left}, #{margin.top})"

        entered = do ((@svg.selectAll '.bar').data @results).enter
        g = (entered.append 'g').attr 'class', 'bar'
        (g.append 'rect').attr do @getRectAttrs
        ((g.append 'text').attr do @getTextAttrs)
            .text (d) -> "#{d[0]} - #{d[2]}%"

    defineXY: =>
        @x = (do d3.scale.ordinal).rangeRoundBands([0, @_size.width], 0.2);
        @y = (do d3.scale.linear).range [@_size.height, 0]
        @x.domain _.map @results, (d) -> d[0]
        @y.domain [0, @scope.data.total_answers]

    getRectAttrs: =>
        x : (d) => @x(d[0])
        y : (d) => @y(d[1])
        width : do @x.rangeBand
        height : (d) => @_size.height - @y(d[1])

    getTextAttrs: =>
        x : (d) => @x(d[0]) + (do @x.rangeBand) / 2
        y : @_size.height - 30
        'text-anchor' : 'middle'


class HBarChart extends BarChart
    defineXY: =>
        @x = (do d3.scale.linear).range [0, @_size.width]
        @y = (do d3.scale.ordinal).rangeRoundBands([0, @_size.height], 0.2);
        @x.domain [0, @scope.data.total_answers]
        @y.domain _.map @results, (d) -> d[0]

    getRectAttrs: =>
        x : 0
        y : (d) => @y(d[0])
        width : (d) => @x(d[1])
        height : do @y.rangeBand

    getTextAttrs: =>
        x : 10
        y : (d) => @y(d[0]) + (do @y.rangeBand) / 2
        'dominant-baseline' : 'central'


angular.module('arte-ww').directive 'dynamicChart', [->
    directive =
        template : '<div></div>'
        replace : yes
        restrict : 'E'
        scope :
            data : '='
        link: (scope, elem, attr) ->
            scope.chart = undefined
            # We instanciate the right chart from data.chart_type
            scope.chart = switch (do scope.data.chart_type.toLowerCase)
                when 'pie' then new PieChart scope, elem
                when 'bar' then new BarChart scope, elem
                when 'hbar' then new HBarChart scope, elem
                else throw "Chart type '#{scope.data.chart_type}' does not exist."
]