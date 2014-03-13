class ResultsCtrl
    @$inject: ['$scope', '$location', 'Thematic', '$http', '$sce']

    changeQuestion: (id) =>
        if (do @Thematic.current)?
            request =
                url : "/api/questions/#{id}"
                method : 'GET'
            @$http(request).success (data) =>
                if (do @Thematic.current).id isnt @$scope.thematics[@$scope.current.thematic].id
                    @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
                @$scope.nochart = false
                @$scope.currentAnswer = data
                @$scope.hasNext = @elements[@$scope.current.thematic][@$scope.current.answer + 1]? or @elements[@$scope.current.thematic + 1]?
                @$scope.hasPrev = @elements[@$scope.current.thematic][@$scope.current.answer - 1]? or @elements[@$scope.current.thematic - 1]?

    constructor: (@$scope, $location, @Thematic, @$http, $sce) ->
        # Update URL when the user changes filters
        @$scope.$watch 'filters', (=>
            f = angular.copy $scope.filters
            $location.search 'gender', null
            if (f.male isnt f.female)
                ($location.search 'gender', 'male') if f.male
                ($location.search 'gender', 'female') if f.female
            $location.search 'age_min', f.age_min
            $location.search 'age_max', f.age_max
        ), yes

        @$scope.hasNext = no
        @$scope.hasPrev = no

        @$scope.current =
            thematic : 0
            answer : 0

        @$scope.getTrustedHTML = =>
            if @$scope.currentAnswer? and @$scope.currentAnswer.feedback?
                $sce.trustAsHtml @$scope.currentAnswer.feedback.html_sentence

        # List all thematics
        @$scope.thematics = []
        @elements = []
        @$scope.$watch (=>
            @Thematic.positionList
        ), =>
            if @Thematic.positionList?
                @$scope.thematics = _.filter (_.map @Thematic.positionList.elements, (thematic, i) =>
                    if thematic.slug isnt 'toi'
                        slug : thematic.slug
                        title : thematic.title
                        id : thematic.id
                        position : i
                    else
                        return
                ), (e) -> e?

                request =
                    url : '/api/thematics-result'
                    method : 'GET'
                (@$http request).success (data) =>
                    @elements = _.filter (_.map data, (thematic) =>
                        if thematic.slug isnt 'toi'
                            _.pluck (_.filter thematic.elements, (t) -> t.type is 'question'), 'object_id'
                        else
                            return
                    ), (e) -> e?
                    @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]

        # Initialize filters (fron URL or default values)
        urlFilters = do $location.search
        @$scope.filters =
            age_min : urlFilters.age_min or 16
            age_max : urlFilters.age_max or 35
            male : if urlFilters.gender isnt 'female' then yes else no
            female : if urlFilters.gender isnt 'male' then yes else no

        # Make sure we can't deselect both genders
        @$scope.filter = (gender) =>
            @$scope.filters[gender] = not @$scope.filters[gender]
            if @$scope.filters.male is @$scope.filters.female is false
                @$scope.filters.male = @$scope.filters.female = true

        # Define Previous and Next behavior
        @$scope.next = =>
            if @elements[@$scope.current.thematic][@$scope.current.answer + 1]?
                ++@$scope.current.answer
            else if @elements[@$scope.current.thematic + 1]?
                ++@$scope.current.thematic
                @$scope.current.answer = 0
            @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]

        @$scope.previous = =>
            if @elements[@$scope.current.thematic][@$scope.current.answer - 1]?
                --@$scope.current.answer
            else if @elements[@$scope.current.thematic - 1]?
                --@$scope.current.thematic
                @$scope.current.answer = @elements[@$scope.current.thematic].length - 1
            @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]

        @$scope.changeThematic = (id) =>
            for index of @$scope.thematics
                if @$scope.thematics[index].id is id
                    @$scope.current.thematic = parseInt index
                    @$scope.current.answer = 0
                    @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
                    return

        @$scope.$watch 'current.thematic', (newValue, oldValue) =>
            if @$scope.thematics? and @$scope.thematics[@$scope.current.thematic]?
                @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
        , yes

angular.module('arte-ww')
.controller('ResultsCtrl', ResultsCtrl)