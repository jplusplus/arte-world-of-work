toStr = (val)-> if typeof val isnt String then ""+val else val

class FeedbackService
    @$inject: ['$http', '$q', 'utils']
    
    constructor: (@http, @q, @utils)->
        @invocations = 0
        @loadedFeedbacks = {}
        @last_feedback_distance = 0

    distanceIsGood: => @last_feedback_distance > 3 

    resetDistance: => @last_feedback_distance = 0

    increaseDistance: => @last_feedback_distance += 1 

    decreaseDistance: => @last_feedback_distance -= 1

    distance: => @last_feedback_distance

    getLoaded: (question_id)=> 
        @loadedFeedbacks[toStr(question_id)]

    setLoaded: (question_id, feedback)=>
        @loadedFeedbacks[toStr(question_id)] = feedback

    getForQuestion: (question_id)=>
        # will load dynamic feedback for 
        deferred = @q.defer()
        unless question_id
            deferred.reject('passed question id is undefined')
        else
            loadedFeedback = @getLoaded(question_id)
            unless loadedFeedback?
                feedback_url = '/api/questions/:question_id/feedback/'.replace(':question_id', toStr(question_id))
                http_promise = @http.get(feedback_url)
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
