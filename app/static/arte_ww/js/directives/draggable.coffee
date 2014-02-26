angular.module('arte-ww').directive "draggable", ['$document', ($document) ->
  (scope, element, attr) ->    
    startX = 0
    startY = 0
    x = 0
    y = 0
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

    element.css "position", "relative" if element.css("position") is "static"

    element.on "mousedown", (event) ->
      event.preventDefault()   
      startX = event.pageX - x
      startY = event.pageY - y
      $document.on "mousemove", mousemove
      $document.on "mouseup", mouseup
]
