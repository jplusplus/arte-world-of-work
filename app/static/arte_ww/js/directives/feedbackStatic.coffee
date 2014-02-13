angular.module('arte-ww').directive 'feedbackStatic', [ '$sce'
    ($sce)->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/feedback-static.html"
            link: (scope, elem, attrs)->
                feedback = scope.$parent.element
                scope.html_sentence = $sce.trustAsHtml(feedback.html_sentence)
                scope.feedback = feedback

]
