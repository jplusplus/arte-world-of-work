# Encoding: utf-8
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-03-26 22:10:06
# Last Modified time: 2014-04-10 11:43:08
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

# extra attributes and method usefull for angular app.
Feedback =
    _wrapped: true 
    shown: false
    hasBeenShown: => @shown
    setShown: => @shown = true
    hasEnoughAnswers: =>
        return false unless @total_answers
        @total_answers >= 15


Question = 
    _wrapped: true
    hasFeedback: => @feedback?



class Utils
    @$inject: ['$http', '$cookies', 'User']

    constructor: (@$http, @$cookies, @User) ->

    # -------------------------------------------------------------------------
    # Utility service for front-end application
    #
    # attributes:
    #    - states: common state name / value shared accross components
    # -------------------------------------------------------------------------
    states:
        survey:
            INTRO: 0
            DOING: 1
            OUTRO: 2
        thematic:
            LANDING : 0
            INTRO   : 1
            ELEMENTS: 2
            FEEDBACK: 3 

    genericWrap: (el, klass_obj)=>
        return el unless el
        return el if el._wrapped
        return _.extend(el, klass_obj)
        

    wrapQuestion: (question)=> 
        question = @genericWrap(question, Question)
        if question and question.hasFeedback()
            question.feedback = @wrapFeedback(question.feedback)
        return question

    wrapFeedback: (feedback)=>
        return @genericWrap(feedback, Feedback)

    authenticate: (callback, create = yes) =>
        createNewUser = =>
            (do @User.post).success (data) =>
                @$cookies['apitoken'] = data.token
                do callback
        if not @$cookies['apitoken']?
            if create
                do createNewUser
            else
                do callback
        else
            request =
                method : 'POST'
                url : '/api/verify-token/'
            ((@$http request).success =>
                do callback
            ).error (error, status) =>
                if status is 401
                    delete @$cookies['apitoken']
                    if create
                        do createNewUser
                    else
                        do callback


angular.module('arte-ww.utils').service('utils', Utils)