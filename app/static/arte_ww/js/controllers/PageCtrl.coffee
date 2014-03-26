class PageCtrl
    @$inject: ['$scope', '$location', '$translate', '$cookies']

    constructor: (@scope, @location, @$translate, @cookies)->
        @title = ''
        @scope.Page = this        

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
