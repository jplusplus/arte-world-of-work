angular.module('arte-ww').directive 'trackThematic', ['Thematic'
    (Thematic)->
        directive =
            restrict: "A"
            link: (scope, elem)->       
                prefix = "thematic-"                                    
                elem.addClass prefix + "argent"
                # Watch changes on the current thematic
                scope.$watch Thematic.current, (thematic)->
                    if thematic?
                        # Cleanup existing classes
                        classList = elem.attr('class').split(/\s+/)
                        $.each  classList, (index, item)->
                            elem.removeClass(item) if item.indexOf(prefix) is 0                     
                        # Add the new one
                        elem.addClass prefix + thematic.slug
]
