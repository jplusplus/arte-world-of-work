module.exports = (grunt)->
    angular_files = [
        'app/arte_ww/static/js/*.coffee',  # our scripts 
        'app/arte_ww/static/js/**/*.coffee',  # our scripts 
        'app/templates/*.html', # our templates     
        'app/templates/partials/*.html' # our templates     
        'app/templates/partials/**/*.html' # our templates     
    ]

    # Project configuration.
    grunt.config.init
        # i18n & angular translate configuration 
        i18nextract:
            dev:
                defaultLang: 'en'
                lang: [ 'en', 'fr', 'de' ]
                src: angular_files
                suffix: ".json"
                dest: "app/static/locale"
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
