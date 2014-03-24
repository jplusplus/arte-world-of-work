angular.module('arte-ww').directive 'feedbackDynamic', [ '$sce'
    ($sce)->
        directive =
            restrict: "AE"
            templateUrl: "partial/directives/feedback-dynamic.html"
            link: (scope, elem, attrs)->
                bindFeedback = ->
                    feedback = scope.$parent.element
                    if typeof feedback.html_sentence is String
                        feedback = _.extend feedback, 
                            html_sentence: $sce.trustAsHtml(feedback.html_sentence)
                    scope.feedback = feedback

                scope.$watch '$parent.element', bindFeedback 
                do bindFeedback

]
