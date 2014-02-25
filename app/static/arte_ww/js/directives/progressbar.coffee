angular.module('arte-ww').directive 'progressbar', ['UserPosition', 'Thematic',
    (UserPosition, Thematic) ->
        directive =
            restrict: "A"
            link: (scope, elem) ->
                thematicElements = []
                elements = 0

                positions =
                    global : 0
                    thematic : 0
                    element : 0

                updateBarWidth = (position) ->
                    if elements > 0
                        percent = "#{position * 100 / elements}%"
                    else
                        percent = 0
                    elem[0].style.width = percent
                    elem[0].innerHTML = percent

                scope.$watch (=>
                    if Thematic.positionList?
                        Thematic.positionList.elements.length
                    else
                        0
                ), ((val) =>
                    if val is 0 then return

                    thematicElements = _.map Thematic.positionList.elements, (e) -> e.elements.length
                    elements = _.reduce thematicElements, ((it, elem) => it + elem), 0

                    updateBarWidth positions.global
                ), yes

                updatePosition = =>
                    positions.global = 0
                    if positions.thematic > 0
                        for i in [0..(positions.thematic - 1)]
                            positions.global += thematicElements[i]
                    positions.global += positions.element
                    updateBarWidth positions.global

                scope.$watch (=> do UserPosition.elementPosition), (newPosition) ->
                    positions.element = newPosition
                    do updatePosition

                scope.$watch (=> do UserPosition.thematicPosition), (newPosition) ->
                    positions.thematic = newPosition
]
