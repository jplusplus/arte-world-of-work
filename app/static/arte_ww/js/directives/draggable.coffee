angular.module('arte-ww').directive "draggable", ['$document', ($document) ->
  (scope, element, attr) ->    
    startX = startY = 0
    x = y = 0
    # Prevent default dragging of selected content
    mousemove = (event) ->
      y = event.pageY - startY
      x = event.pageX - startX
      element.css
        top:  y + "px"
        left: x + "px"

    mouseup = ->
      $document.unbind "mousemove", mousemove
      $document.unbind "mouseup", mouseup
      if attr.restore?
        x = y = 0
        element.animate { top: 0, left: 0 }, 400

    element.css "position", "relative" if element.css("position") is "static"

    element.on "mousedown", (event) ->
      event.preventDefault()   
      startX = event.pageX - x
      startY = event.pageY - y
      $document.on "mousemove", mousemove
      $document.on "mouseup", mouseup
]
