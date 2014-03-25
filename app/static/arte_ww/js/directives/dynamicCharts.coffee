class Chart
    constructor: (@scope, @element) ->
        # Create the svg element
        @svg = (d3.select @element[0]).selectAll 'svg'

        # Create a color range
        @color = (do d3.scale.category20)

        @layout = undefined

        do @setSize

    computeResults: =>
        # Compute the result into something usable by the layout
        @results = []
        _.forEach (_.keys @scope.data.results), (key) =>
            @results.push [@scope.data.sets[key].title, @scope.data.results[key]]

    setSize: =>
        @size =
            width : do @element.width
            height : do @element.height

        ((d3.select @element[0]).selectAll 'svg').attr
            width : @size.width
            height : @size.height

    update: =>
        do @computeResults

    delete: =>
        do (((d3.select @element[0]).selectAll 'svg').selectAll '*').remove

class PieChart extends Chart
    constructor: (@scope, @element) ->
        super @scope, @element

        @type = 'pie'

        # Create the layout
        @layout = do d3.layout.pie
        @layout.value (d) -> d[1]

        # Create arcs
        radius = (Math.min @size.width, @size.height) / 2 - 10
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
            .text (d) ->
                if d.data[1] > 0 then "#{d.data[0]} - #{d.data[1]}%" else ""


class BarChart extends Chart
    constructor: (@scope, @element) ->
        @margin = @margin or
            top : 0
            right : 0
            bottom : 50
            left : 0

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
            .text (d) -> "#{d[1]}%"

        do @appendLegend

    appendLegend: =>
        do (@svg.selectAll '.legend').remove

        data = (@svg.selectAll '.legend').data @results
        entered = do data.enter

        fObject = (entered.append 'foreignObject').attr
            class : 'legend'
            width : do @x.rangeBand
            height : @margin.bottom
            x : (d) => @x(d[0])
            y : @size.height - @margin.bottom
        (fObject.append 'xhtml:body').html (d) => "<p>#{d[0]}</p>"

    defineXY: =>
        @x = (do d3.scale.ordinal).rangeRoundBands([0, @_size.width], 0.2);
        @y = (do d3.scale.linear).range [@_size.height, 0]
        @x.domain _.map @results, (d) -> d[0]
        @y.domain [0, _.max _.values @scope.data.results]

    getRectAttrs: =>
        x : (d) => @x(d[0])
        y : (d) => @y(d[1])
        width : do @x.rangeBand
        height : (d) => @_size.height - @y(d[1])

    getTextAttrs: =>
        x : (d) => @x(d[0]) + (do @x.rangeBand) / 2
        y : @_size.height - 10
        'text-anchor' : 'middle'


class HBarChart extends BarChart
    constructor: (@scope, @element) ->
        @margin =
            top : 0
            right : 10
            bottom : 0
            left : 10

        super @scope, @element

        @type = 'hbar'

    defineXY: =>
        @x = (do d3.scale.linear).range [0, @_size.width]
        @y = (do d3.scale.ordinal).rangeRoundBands([0, @_size.height], 0.5, 0);
        @x.domain [0, _.max _.values @scope.data.results]
        @y.domain _.map @results, (d) -> d[0]

    getRectAttrs: =>
        x : 0
        y : (d) => @y(d[0])
        width : (d) => @x(d[1])
        height : do @y.rangeBand

    getTextAttrs: =>
        x : 5
        y : (d) => @y(d[0]) + (do @y.rangeBand) / 2
        'dominant-baseline' : 'central'
        class : (d) -> if (parseInt d[1]) is 0 then 'zero' else ' '

    appendLegend: =>
        do (@svg.selectAll '.legend').remove

        data = (@svg.selectAll '.legend').data @results
        entered = do data.enter

        cssclass = if entered[0].length >= 6 then 'legend small' else 'legend'

        fObject = (entered.append 'foreignObject').attr
            class : cssclass
            width : @_size.width
            height: do @y.rangeBand
            x : 0
            y : (d) => @y(d[0]) - 2 + do @y.rangeBand
        (fObject.append 'xhtml:body').html (d) => "<p>#{d[0]}</p>"

class Histogram extends BarChart
    constructor: (@scope, @element) ->
        @margin =
            top : 20
            right : 20
            bottom : 20
            left : 20

        super @scope, @element

    update: =>
        super ''

        ((((d3.select @element[0]).selectAll 'svg').append 'g').attr
            class : 'x axis'
            transform : "translate(#{@margin.left}, #{@size.height - @margin.bottom})"
        ).call @xAxis

    computeResults: =>
        @results = []
        _.forEach (_.keys @scope.data.results), (key) =>
            percent = parseInt (@scope.data.results[key] * 100 / @scope.data.total_answers + 0.5)
            @results.push [@scope.data.sets[key].min, @scope.data.sets[key].max, @scope.data.results[key], percent]

    defineXY: =>
        @x = (do d3.scale.linear).range [0, @_size.width];
        @y = (do d3.scale.linear).range [@_size.height, 0]
        @x.domain [0, (_.max @results, (elem) -> elem[1])[1]]
        @y.domain [0, @scope.data.total_answers]

        tickValues = [0].concat _.pluck @results, 1
        @xAxis = (((do d3.svg.axis).scale @x).orient 'bottom').tickValues tickValues
        @xAxis.tickFormat (d3.format 'f')

    getTextAttrs: =>
        display: 'none'

    getRectAttrs: =>
        x : (d) => (@x d[0])
        y : (d) => (@y d[2])
        width : (d) => (@x d[1]) - (@x d[0])
        height : (d) => @_size.height - @y(d[2])

    appendLegend: =>


angular.module('arte-ww').directive 'dynamicChart', ['$window', 'Result', '$rootScope', ($window, $Result, $rootScope) ->
    directive =
        templateUrl : 'partial/directives/chart.html'
        replace : yes
        restrict : 'E'
        scope :
            id : '@'
            filters : '='
            nochart : '@'
        controller : ['$scope', (scope) ->
            scope.filter =
                from : 0
                to : 99
                h : yes
                f : yes
        ]
        link: (scope, elem, attr) ->
            newChart = =>
                # We instanciate the right chart from data.chart_type
                scope.chart = switch (do scope.data.chart_type.toLowerCase)
                    when 'pie' then new PieChart scope, elem
                    when 'bar' then new BarChart scope, elem
                    when 'horizontal_bar' then new HBarChart scope, elem
                    when 'histogramme' then new Histogram scope, elem
                    else throw "Chart type '#{scope.data.chart_type}' does not exist."

            update = =>
                return if not scope.id? or scope.id is "" or scope.id < 0

                filters = angular.copy scope.filters
                if filters.male isnt filters.female
                    filters.gender = 'male' if filters.male
                    filters.gender = 'female' if filters.female
                delete filters.male
                delete filters.female

                request =
                    id : scope.id
                    filters : filters
                $Result.get request, (data) =>
                    scope.$parent.fullwidth = no
                    scope.$parent.nochart = no


                    if data.results.total_answers < 5
                        scope.$parent.nochart = yes
                    else if data.results.chart_type is 'horizontal_bar'
                        scope.$parent.fullwidth = yes
                    scope.data = data.results
                    $rootScope.isThematicLoading = no
                undefined

            window.onresize = =>
                do scope.$apply

            scope.chart = undefined

            # Watch resize events
            scope.$watch =>
                return (angular.element $window)[0].innerWidth
            , =>
                if scope.chart?
                    do scope.chart.setSize
                    do scope.chart.update

            # Watch changes in the data
            scope.$watch 'data', (newValues, oldValues) =>
                if scope.data?
                    if scope.chart? and scope.chart.type isnt (do scope.data.chart_type.toLowerCase)
                        do scope.chart.delete
                        scope.chart = undefined
                        do newChart
                    else if not scope.chart?
                        do newChart
                    do scope.chart.update
            , yes

            # Watch changes in the filters
            scope.$watch 'filters', (newValues, oldValues) =>
                do update
            , yes

            scope.$watch 'id', =>
                do update
            , yes

]