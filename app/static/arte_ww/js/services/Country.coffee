class CountryService
    @$inject: ['$http']

    constructor: (@$http) ->
        @list = []
        @listCountries (countries)=>
            @list = countries

    listCountries: (cb)=>
        request =
            method : 'GET'
            url : "/api/countries/"
        (@$http request).success cb

angular.module('arte-ww.services').service 'Country', CountryService