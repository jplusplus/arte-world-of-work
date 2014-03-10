class ThirdPartyService
    @$inject: ['$http', '$window']

    constructor: (@http, @window) -> # YOLO
        url = "http://jplusplus.org" # @window.location.hostname        
        # Get shares count from facebook
        @getFacebookCount(url)
        @getTwitterCount(url)
        @getGplusCount(url)

    getFacebookCount: (url)=>
        @http.jsonp("http://graph.facebook.com/#{url}?callback=JSON_CALLBACK").then (body)=>             
            @facebookCount = body.data.shares or 0

    getTwitterCount: (url)=>
        @http.jsonp("http://urls.api.twitter.com/1/urls/count.json?callback=JSON_CALLBACK&url=#{url}").then (body)=>                       
            @twitterCount = body.data.count or 0

    getGplusCount: (url)=>
        @http.get("/api/gplus-count?url=#{url}").then (body)=>                       
            @gplusCount = body.data.count or 0


(angular.module 'arte-ww.services').service 'ThirdParty', ThirdPartyService