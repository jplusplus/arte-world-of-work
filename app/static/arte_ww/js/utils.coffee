# extra attributes and method usefull for angular app.
Feedback =
    _wrapped: true 
    shown: false
    hasBeenShown: => @shown
    setShown: => @shown = true
    hasEnoughAnswers: =>
        return false unless @total_answers
        @total_answers >= 300 


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