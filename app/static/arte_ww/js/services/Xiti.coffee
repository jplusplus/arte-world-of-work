# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-27 16:19:29
# Last Modified time: 2014-04-10 12:26:25
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

angular.module('arte-ww.services').service 'Xiti', ['$cookies', ($cookies)->
    new class Xiti
        config:
            fr:
                xtsite: "428435"
                xtn2  : "1"
                prefix:  "dos_europe::fr::dos_wow::"
            de:
                xtsite: "428450"
                xtn2  : "2"     
                prefix:  "dos_europe::de::dos_wow::"       
            en:
                xtsite: "431209"
                xtn2  : "2"
                prefix:  "dos_europe::en::dos_wow::"

        constructor:->     
            do @updateConfig
            # Load xiti script
            do @loadScript

        getConfig:=> @config[$cookies.django_language or "en"]           

        updateConfig: =>
            config          = @getConfig()
            # Xiti's core variables
            window.xtnv     = document
            window.xtsd     = config.xtsd   or "http://logi104"
            window.xtsite   = config.xtsite or "428435" # site number
            window.xtn2     = config.xtn2   or "1"      # level 2 site            
            window.xtpage   = ""                        # page name (with the use of :: to create chapters)
            window.xtdi     = ""                        # implication degree
            window.xt_multc = ""                        # customized indicators
            window.xt_an    = ""                        # numeric identifier
            window.xt_ac    = ""                        # category

            window.xtparam = "" unless window.xtparam?
            window.xtparam += "&ac=" + xt_ac + "&an=" + xt_an + xt_multc            

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
                xtpage       = @getConfig().prefix + @currentPage
                # Destroy existing image
                angular.element( @img ).remove() if @img?
                # Create the new image
                @img        = document.createElement("img")
                @img.height = 1
                @img.width  = 1
                @img.src    = "#{window.xtsd}.xiti.com/"
                @img.src   += "hit.xiti?s=#{window.xtsite}"
                @img.src   += "&s2=2"
                @img.src   += "&p=#{xtpage}"
                @img.src   += "&di=#{window.xtdi}"
                # Appends the image to the body
                angular.element("body").append @img

        trackClick: (ev, name, level=window.xtn2)->      
            window.xt_click(ev.target, 'C', level, name,'N')        
            yes        

]