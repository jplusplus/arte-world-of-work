angular.module('arte-ww').directive 'trackThematic', ['Thematic'
    (Thematic)->
        # Constantes
        PREFIX  = "thematic-"   
        DEFAULT = "toi"   

        directive =
            restrict: "A"
            link: (scope, elem)->       
                elem.addClass PREFIX + DEFAULT
                # Watch changes on the current thematic
                scope.$watch Thematic.current, (thematic)->                 
                    if thematic?
                        # Cleanup existing classes
                        classList = elem.attr('class').split(/\s+/)
                        $.each  classList, (index, item)->
                            elem.removeClass(item) if item.indexOf(PREFIX) is 0                     
                        # Add the new one
                        elem.addClass PREFIX + thematic.slug
]
