# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-24 12:40:40
# Last Modified time: 2014-04-10 11:43:36
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

class AnswerService
    @$inject: ['$http']

    constructor: (@$http) ->
        @answers = []
        @listMyAnswers (answer_list)=>
            _.each answer_list, @addAnswer

    onAnswerError: (error)=>
        console.log "[arte_ww.services.Answer] Error happened while answering" ,error

    addAnswer: (answer)=>
        @answers[answer.question] = answer

    getAnswerForQuestion: (question_id)=>
        return @answers[ question_id ]

    deleteAnswerForQuestion: (question_id) =>
        if @answers[question_id]?
            (@delete @answers[question_id]).success (data) =>
                delete @answers[question_id]

    listMyAnswers: (cb)=>
        request =
            method : 'GET'
            url : "/api/my-answers/"
        (@$http request).success cb

    answer: (params, cb)=>
        ###
        Main method of this service, used to answer a specific question. If 
        answer already exist then we update it.

        Arguments:

            - params{Object} – Request parameters
                + question{Number} – The question id to answer
                + value{Array|Number} – The answer value
              
            - cb{Object} – Request callback            
                + succes{Function} – function called on success   
                + error{Function}  – function called on error
        ### 
        previousAnswer = @getAnswerForQuestion( params.question )
        if previousAnswer
            promise = @update previousAnswer, params
        else
            promise = @post params 

        promise.success (data)=>
            @addAnswer(data)
            cb.success(data) if cb? and angular.isFunction cb.success

        promise.error (data)=>
            @onAnswerError(data)
            cb.error(data) if cb? and angular.isFunction cb.error

        return promise

    delete: (answer) =>
        request =
            method : 'DELETE'
            url : "/api/answers/#{answer.id}/"

        @$http request

    post: (params) =>
        request =
            method: 'POST'
            url : '/api/answers/'
            data: params

        @$http request

        
    update: (answer, params)=>

        request =
            method: 'PUT'
            url : "/api/answers/#{answer.id}/"
            data: params

        @$http request


(angular.module 'arte-ww.services').service 'Answer', AnswerService