angular.module('arte-ww').directive 'progressbar', ['UserPosition', 'Thematic', 'utils',
    (UserPosition, Thematic, utils) ->
        directive =
            restrict: "A"
            link: (scope, elem) ->
                elements = 0

                getElementPosition = ->
                    do UserPosition.elementPosition

                updateBarWidth = (position) ->
                    percent = "#{position * 100 / elements}%"
                    elem[0].style.width = percent
                    elem[0].innerHTML = percent

                scope.$watch getElementPosition, (position) ->
                    if elements > 0
                        updateBarWidth position
                    else
                        elem[0].style.width = 0

                scope.$watch (=>
                    do UserPosition.currentState
                ), (state) =>
                    if state is utils.states.thematic.OUTRO
                        updateBarWidth elements
                    else
                        updateBarWidth do UserPosition.elementPosition

                scope.$watch Thematic.current, (thematic) ->
                    if thematic?
                        elements = thematic.elements.length
                        if elements > 0
                            updateBarWidth do UserPosition.elementPosition
]
