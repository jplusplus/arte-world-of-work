class PageCtrl
    @$inject: ['$scope', '$location', '$translate']

    constructor: (@scope, @location, @$translate)->
        @title = @$translate('World of Work')
        @scope.Page = this

        params = @location.search()
        if params.lang
            @langChanged params.lang


        @scope.$watch ->
            @location.search().lang if @location
        , @langChanged

    langChanged: (lang)=>
        return unless lang
        @$translate.use(lang)

    title: (title) =>
        if title?
            @title = title
        @title 

    currentLang: (lang)=>
        if lang?
            @langChanged(lang)
        @$translate.use()



angular.module('arte-ww').controller 'PageCtrl', PageCtrl
