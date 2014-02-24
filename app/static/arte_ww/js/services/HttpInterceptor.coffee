angular.module('arte-ww.services').factory('HttpInterceptor', [ '$q', '$cookies', ($q, $cookies)->
    request: (config)->
        config = config or $q.when(config)
        # Add CSRF Token for post request
        if $cookies.csrftoken?
            config.headers = config.headers or {}
            config.headers['X-CSRFToken'] = $cookies.csrftoken
        # do something on success
        return config
])
