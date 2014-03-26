angular.module('arte-ww.services').service 'Xiti', ['$cookies', ($cookies)->
    new class Xiti
        constructor:->
            @currentPage    = null
            # Xiti's core variables
            window.xtnv     = document
            window.xtsd     = "http://logi104"
            window.xtsite   = "428435"                  # site number
            window.xtn2     = "1"                       # level 2 site            
            window.xtpage   = ""                        # page name (with the use of :: to create chapters)
            window.xtdi     = ""                        # implication degree
            window.xt_multc = ""                        # customized indicators
            window.xt_an    = ""                        # numeric identifier
            window.xt_ac    = ""                        # category

            window.xtparam = "" unless window.xtparam?
            window.xtparam += "&ac=" + xt_ac + "&an=" + xt_an + xt_multc            
            # Load xiti script
            @loadScript()

        getPrefix: ->            
            lang = $cookies.django_language or "en"
            "dos_europe::#{lang}::dos_wow::"


        loadScript: ->            
            at = document.createElement("script")
            at.type = "text/javascript"
            at.async = true
            at.src = "http://www.arte.tv/guide/javascripts/xtcore.js"
            angular.element("header").append(at)

        loadPage: =>
            # Convert arguments object to an array
            args = Array.prototype.slice.call(arguments)            
            # Current page must be different
            if @currentPage isnt args.join("::")
                # Record the current page slug to avoid declare the page twice
                @currentPage = args.join("::")
                # Create xtpage slug
                xtpage       = @getPrefix() + @currentPage
                # Destroy existing image
                angular.element( @img ).remove() if @img?
                # Create the new image
                @img        = document.createElement("img")
                @img.height = 1
                @img.width  = 1
                @img.src    = "#{window.xtsd}.xiti.com/"
                @img.src   += "hit.xiti?s=#{window.xtsite}"
                @img.src   += "&amp;s2=2"
                @img.src   += "&amp;p=#{xtpage}"
                @img.src   += "&amp;di=#{window.xtdi}"
                # Appends the image to the body
                angular.element("body").append @img
                
                
]