class Chart
    constructor: (@scope, @element) ->
        # Create the svg element
        @svg = (d3.select @element[0]).append 'svg'

        # Create a color range
        @color = (do d3.scale.category20)

        @layout = undefined

        do @setSize

    computeResults: =>
        # Compute the result into something usable by the pie layout
        @results = []
        _.forEach (_.keys @scope.data.results), (key) =>
            percent = parseInt (@scope.data.results[key] * 100 / @scope.data.total_answers + 0.5)
            @results.push [key, @scope.data.results[key], percent]

    setSize: =>
        @size =
            width : do @element.width
            height : do @element.height

        @svg.attr
            width : @size.width
            height : @size.height

    update: =>
        do @computeResults

    delete: =>
        do ((d3.select @element[0]).selectAll 'svg').remove

class PieChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

        @type = 'pie'

        # Create the layout
        @layout = do d3.layout.pie
        @layout.value (d) -> d[1]

        # Create arcs
        radius = (Math.min @size.width, @size.height) / 2
        @arc = do d3.svg.arc
        @arc.outerRadius radius
        @arc.innerRadius 0

        # Center the pie
        @svg = (@svg.append 'g').attr 'transform', "translate(#{@size.width / 2}, #{@size.height / 2})"

    update : =>
        super ''

        # Remove old arcs
        do (@svg.selectAll '.arc').remove

        # Get all e1ntering data
        g = (do ((@svg.selectAll '.arc').data (@layout @results)).enter).append 'g'
        g.attr 'class', 'arc'

        # Append the path
        ((g.append 'path').attr 'd', @arc).style 'fill', (d) => @color d.data[0]

        # And append the text
        (g.append 'text')
            .attr
                transform : (d) => "translate(#{@arc.centroid d})"
            .style
                'text-anchor' : 'middle'
            .text (d) -> "#{d.data[0]} - #{d.data[2]}%"


class BarChart extends Chart
    constructor: (@scope, @element) ->
        @margin =
            top : 20
            right : 10
            bottom : 20
            left : 10

        super @scope, @element

        @type = 'bar'

        @svg = (@svg.append 'g')
            .attr 'transform', "translate(#{@margin.left}, #{@margin.top})"

    update : =>
        super ''

        @_size =
            width : @size.width - @margin.right - @margin.left
            height : @size.height - @margin.top - @margin.bottom

        # Compute scales
        do @defineXY

        # Remove old rects
        do (@svg.selectAll '.bar').remove

        data = (@svg.selectAll '.bar').data @results

        entered = do data.enter
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
    constructor: (@scope, @element) ->
        super @scope, @element

        @type = 'hbar'

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
            newChart = =>
                # We instanciate the right chart from data.chart_type
                scope.chart = switch (do scope.data.chart_type.toLowerCase)
                    when 'pie' then new PieChart scope, elem
                    when 'bar' then new BarChart scope, elem
                    when 'hbar' then new HBarChart scope, elem
                    else throw "Chart type '#{scope.data.chart_type}' does not exist."

            window.onresize = =>
                do scope.$apply

            scope.chart = undefined

            scope.$watch =>
                return (angular.element window)[0].innerWidth
            , =>
                if scope.chart?
                    do scope.chart.setSize
                    do scope.chart.update

            scope.$watch 'data', (newValues, oldValues) =>
                if scope.chart? and scope.chart.type isnt (do scope.data.chart_type.toLowerCase)
                    do scope.chart.delete
                    do newChart
                do scope.chart.update
            , yes


            do newChart

]