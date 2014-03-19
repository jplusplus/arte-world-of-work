# extra attributes and method usefull for angular app.
Feedback =
    shown: false
    hasBeenShown: => @shown
    setShown: => @shown = true
    hasEnoughAnswers: => 
        return false unless @total_answers
        @total_answers >= 300 


class FeedbackService
    # Dependencies injection
    @$inject: ['$http', '$q']
    
    constructor: (@http, @q)->
        @loadedFeedbacks = {}
        @last_feedback_distance = 0

    # Single method config
    feedbackConfig: 
        url: '/api/questions/:question_id/feedback'
        method: 'GET'

    isDistanceFarEnought: => @last_feedback_distance > 3 

    resetDistance: => @last_feedback_distance = 0

    increaseDistance: => @last_feedback_distance += 1 

    decreaseDistance: => @last_feedback_distance -= 1

    distance: => @last_feedback_distance

    getLoaded: (question_id)=> 
        key = ""+question_id # String casting
        @loadedFeedbacks[key]

    setLoaded: (question_id, feedback)=>
        key = ""+question_id # String casting
        @loadedFeedbacks[key] = feedback

    getForQuestion: (question_id)=>
        deferred = @q.defer()
        unless question_id
            deferred.reject('passed question id is undefined')
        else
            loadedFeedback = @getLoaded(question_id)
            console.log "loadedFeedback: ", loadedFeedback

            unless loadedFeedback?
                config = _.extend @feedbackConfig,
                    url: @feedbackConfig.url.replace(':question_id', question_id)
                http_promise = @http(config)
                http_promise.success (feedback)=>
                    # adding extra utility methods for this feedback 
                    feedback = _.extend feedback, Feedback
                    @setLoaded(question_id, feedback)
                    deferred.resolve(feedback)

                http_promise.error (error)->
                    deferred.reject(error)
            else
                deferred.resolve(loadedFeedback)

        return deferred.promise

angular.module('arte-ww.services').service 'Feedback', FeedbackService
