# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# Licence: GNU General Public Licence
# -----------------------------------------------------------------------------
# Creation time:      2014-04-03 13:30:07
# Last Modified time: 2014-04-10 12:14:32
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

module.exports = (grunt)->
    angular_files = [
        # our scripts 
        'app/static/arte_ww/js/*.coffee'
        'app/static/arte_ww/js/**/*.coffee'
        # our templates      
        'app/templates/*.html'
        'app/templates/partials/*.html'
        'app/templates/partials/**/*.html'
    ]

    # Project configuration.
    grunt.config.init
        # i18n & angular translate configuration 
        i18nextract:
            dev:
                defaultLang: 'en'
                lang: [ 'en', ]
                src: angular_files
                suffix: ".json"
                dest: "app/static/arte_ww/locale"
                interpolation: 
                    startDelimiter: '[['
                    endDelimiter: ']]'
        # auto generate i18n json files 
        watch:
            i18n:
                files: angular_files
                tasks: ['makemessages']
        


    # Load the angular translate task
    grunt.loadNpmTasks('grunt-angular-translate')
    grunt.loadNpmTasks('grunt-available-tasks')
    grunt.loadNpmTasks('grunt-contrib-watch')

    grunt.registerTask 'makemessages', 'i18nextract:dev' 
    grunt.registerTask 'default', ['available_tasks']
