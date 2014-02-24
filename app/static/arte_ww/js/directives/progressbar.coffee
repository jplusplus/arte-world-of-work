angular.module('arte-ww').directive 'progressbar', ['UserPosition', 'Thematic',
    (UserPosition, Thematic) ->
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

                scope.$watch Thematic.current, (thematic) ->
                    if thematic?
                        elements = thematic.elements.length
                        if elements > 0
                            updateBarWidth do UserPosition.elementPosition
]
