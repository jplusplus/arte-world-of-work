# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-27 16:19:29
# Last Modified time: 2014-04-10 12:26:38
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

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
