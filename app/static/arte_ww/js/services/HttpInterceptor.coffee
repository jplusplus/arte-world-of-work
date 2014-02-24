isApi = (url) -> ((url.indexOf 'api') is 0) or (url.indexOf '/api') is 0

angular.module('arte-ww.services').factory('HttpInterceptor', [ '$q', '$cookies', ($q, $cookies)->
    request: (config)->
        config = config or $q.when(config)
        # Add CSRF Token for post request
        if $cookies.csrftoken?
            config.headers = config.headers or {}
            config.headers['X-CSRFToken'] = $cookies.csrftoken
        # Add API Token if needed
        if (isApi config.url) and $cookies.apitoken?
            config.headers = config.headers or {}
            config.headers['Authorization'] = "Token #{$cookies.apitoken}"
        # do something on success
        return config
])
