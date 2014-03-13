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
            url : "/api/answers/#{answer.id}"

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