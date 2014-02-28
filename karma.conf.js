// Karma configuration
// Generated on Thu Feb 06 2014 17:12:33 GMT+0100 (CET)

module.exports = function(config) {
  config.set({

    // base path, that will be used to resolve files and exclude
    basePath: '',


    // frameworks to use
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'app/static/arte_ww/vendor/underscore/underscore.js',
      'app/static/arte_ww/vendor/angular/angular.js',
      'app/static/arte_ww/vendor/jquery/jquery.min.js',
      'app/static/arte_ww/vendor/angular-sanitize/angular-sanitize.js',
      'app/static/arte_ww/vendor/angular-resource/angular-resource.js',
      'app/static/arte_ww/vendor/angular-cookies/angular-cookies.js',
      'app/static/arte_ww/vendor/angular-mocks/angular-mocks.js',
      'app/static/arte_ww/vendor/angular-animate/angular-animate.min.js',
      'app/static/arte_ww/vendor/angular-translate/angular-translate.js',
      'app/static/arte_ww/vendor/angular-translate-loader-static-files/angular-translate-loader-static-files.js',
      'app/static/arte_ww/vendor/angular-ui-bootstrap-bower/ui-bootstrap.js',
      'app/static/arte_ww/vendor/angular-route/angular-route.js',
      'app/static/arte_ww/vendor/nouislider/jquery.nouislider.js',
      'app/static/arte_ww/vendor/angular-nouislider/nouislider.min.js',
      'app/static/arte_ww/js/*',
      'app/static/arte_ww/js/*/*',
      'app/static/arte_ww/tests/*.coffee',
    ],


    // list of files to exclude
    exclude: [
      
    ],


    // test results reporter to use
    // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera (has to be installed with `npm install karma-opera-launcher`)
    // - Safari (only Mac; has to be installed with `npm install karma-safari-launcher`)
    // - PhantomJS
    // - IE (only Windows; has to be installed with `npm install karma-ie-launcher`)
    browsers: ['Chrome'],


    // If browser does not capture in given timeout [ms], kill it
    captureTimeout: 60000,


    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: true
  });
};
