# TODO: handle user position saving and loading/intialization
class UserPosition: 
    
    constructor: ($rootScope, $resource)->
        @base_user_url = '/api/user/myposition'

        @element_position = 0 
        @thematic_position = 0

        @service = $resource @base_user_url, {},

