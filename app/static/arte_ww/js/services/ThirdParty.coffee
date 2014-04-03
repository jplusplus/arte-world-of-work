angular.module('arte-ww.services').service 'ThirdParty', ['$http', '$window', '$translate', '$cookies', ($http, $window, $translate, $cookies) -> 
    new class ThirdPartyService
        defaultShareLang: 'fr'
        shareUrl: 
            fr: "http://europe.arte.tv/fr/evenements/world-of-work/"
            de: "http://europe.arte.tv/de/veranstaltungen/world-of-work/"

        constructor: ($http, $window, $translate, $cookies) -> # YOLO
            @url   = @getURL() # $window.location.hostname         
            # Get shares count from facebook
            @getFacebookCount(@url)
            @getTwitterCount(@url)
            @getGplusCount(@url)

        getURL: =>
            lang = $cookies.django_language or $translate.use() 
            console.log "lang=", lang
            return @shareUrl[lang] or @shareUrl[@defaultShareLang]

        getFacebookCount: (url=@url)=>
            $http.jsonp("http://graph.facebook.com/#{url}?callback=JSON_CALLBACK").then (body)=>             
                @facebookCount = body.data.shares or 0

        getTwitterCount: (url=@url)=>
            $http.jsonp("http://urls.api.twitter.com/1/urls/count.json?callback=JSON_CALLBACK&url=#{url}").then (body)=>                       
                @twitterCount = body.data.count or 0

        getGplusCount: (url=@url)=>
            $http.get("/api/gplus-count?url=#{url}").then (body)=>                       
                @gplusCount = body.data.count or 0

        shareOnFacebook: (url=@url)=>        
            shareUrl = "https://www.facebook.com/sharer/sharer.php?u=#{url}&display=popup"
            $window.open shareUrl, "shareOnFacebook","menubar=no, status=no, scrollbars=no, menubar=no, width=670, height=370"
            yes # https://github.com/angular/angular.js/issues/4853#issuecomment-28491586

        shareOnTwitter: (url=@url)=>
            # Duplicate string for auto-collection:
            # $translate('Eat, work and sleep? Not quite! Learn about your generation's world of work at {URL} #artewow')
            tweet = $translate.instant("Eat, work and sleep? Not quite! Learn about your generation's world of work at {URL} #artewow") 
            tweet = tweet.replace "{URL}", @url   
            tweet = encodeURIComponent tweet
            shareUrl = "https://twitter.com/share?&text=#{tweet}&url=&"
            $window.open shareUrl, "shareOnTwitter","menubar=no, status=no, scrollbars=no, menubar=no, width=550, height=380"
            yes # https://github.com/angular/angular.js/issues/4853#issuecomment-28491586

        shareOnGplus: (url=@url)=>
            shareUrl = "https://plus.google.com/share?url=#{url}"
            $window.open shareUrl, "shareOnGplus","menubar=no, status=no, scrollbars=no, menubar=no, width=600, height=600"
            yes # https://github.com/angular/angular.js/issues/4853#issuecomment-28491586
]