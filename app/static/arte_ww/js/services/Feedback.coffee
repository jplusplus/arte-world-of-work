

class FeedbackService
    # Dependencies injection
    @$inject: ['$http', '$q', 'utils']
    
    constructor: (@http, @q, @utils)->
        @loadedFeedbacks = {}
        @last_feedback_distance = 0

    # Single method config
    feedbackConfig: 
        url: '/api/questions/:question_id/feedback'
        method: 'GET'

    distanceIsGood: => @last_feedback_distance > 3 

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
            unless loadedFeedback?
                config = _.extend @feedbackConfig,
                    url: @feedbackConfig.url.replace(':question_id', question_id)
                http_promise = @http(config)
                http_promise.success (feedback)=>
                    # adding extra utility methods for this feedback 
                    feedback = @utils.wrapFeedback(feedback)
                    @setLoaded(question_id, feedback)
                    deferred.resolve(feedback)

                http_promise.error (error)->
                    deferred.reject(error)
            else
                deferred.resolve(loadedFeedback)

        return deferred.promise

angular.module('arte-ww.services').service 'Feedback', FeedbackService
