# The about controller doesn't have a proper behavior, it justs provide all 
# required links in every specific language
class AboutCtrl
    @$inject: ['$scope', '$translate']

    links: 
        privacy: 
            de: "http://www.arte.tv/sites/de/aktuelles/datenschutzerklarung-personenbezogener-daten/"
            fr: "http://www.arte.tv/sites/fr/services/declaration-de-protection-des-donnees-personnelles/"

        credits:
            de: "http://www.arte.tv/sites/de/aktuelles/impressum/"
            fr: "http://www.arte.tv/sites/fr/services/credits/"
        terms: 
            de: "http://www.arte.tv/sites/de/aktuelles/allgemeine-nutzungsbedingungen/"
            fr: "http://www.arte.tv/sites/fr/services/conditions-generales-dutilisation/"

    constructor: (@scope, @translate)->
        @scope.getLink = @getLink

    getLink: (name)=>
        used_lang = @translate.use()
        link = @links[name]
        link[used_lang] or link['fr']


angular.module('arte-ww').controller 'AboutCtrl', AboutCtrl
