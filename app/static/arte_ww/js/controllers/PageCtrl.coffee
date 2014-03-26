class PageCtrl
    @$inject: ['$scope', '$location', '$translate', '$cookies']

    constructor: (@scope, @location, @$translate, @cookies)->
        @title = ''

        @scope.Page = this        
        @scope.currentLang = @currentLang
        
        if @cookies.django_language
            @langChanged(@cookies.django_language)

    langChanged: (lang)=>
        return unless lang
        @$translate.use(lang)
        @cookies.django_language = lang

    currentLang: (lang)=>
        if lang?
            @langChanged(lang)
        @$translate.use()

    title: (title) =>
        if title?
            @title = title
        @title 

angular.module('arte-ww').controller 'PageCtrl', PageCtrl
