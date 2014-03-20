class PageCtrl
    @$inject: ['$scope', '$location', '$translate', '$cookies']

    constructor: (@scope, @location, @$translate, @cookies)->
        @title = ''
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
        @cookies.django_language = lang


    title: (title) =>
        if title?
            @title = title
        @title 

    currentLang: (lang)=>
        if lang?
            @langChanged(lang)
        @$translate.use()

angular.module('arte-ww').controller 'PageCtrl', PageCtrl
