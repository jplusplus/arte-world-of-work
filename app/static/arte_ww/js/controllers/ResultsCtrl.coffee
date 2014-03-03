class ResultsCtrl
    @$inject: ['$scope', '$location', 'Thematic', '$http']

    changeQuestion: (id) =>
        request =
            url : "/api/questions/#{id}"
            method : 'GET'
        @$http(request).success (data) =>
            @$scope.currentAnswer = data

    constructor: (@$scope, $location, Thematic, @$http) ->
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

        @$scope.current =
            thematic : 0
            answer : 0

        # List all thematics
        @$scope.thematics = []
        @$scope.$watch (=>
            Thematic.positionList
        ), =>
            if Thematic.positionList?
                @elements = _.map Thematic.positionList.elements, (thematic) =>
                    thematic.elements
                @$scope.thematics = _.map Thematic.positionList.elements, (thematic) =>
                    slug : thematic.slug
                    title : thematic.title

                @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]


        # Initialize filters (fron URL or default values)
        urlFilters = do $location.search
        @$scope.filters =
            age_min : urlFilters.age_min or 0
            age_max : urlFilters.age_max or 99
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

        @$scope.hasNext = =>
            return no if not @elements? or @elements.length is 0
            return @elements[@$scope.current.thematic][@$scope.current.answer + 1]? or @elements[@$scope.current.thematic + 1]?

        @$scope.hasPrev = =>
            return no if not @elements? or @elements.length is 0
            return @elements[@$scope.current.thematic][@$scope.current.answer - 1]? or @elements[@$scope.current.thematic - 1]?

angular.module('arte-ww')
.controller('ResultsCtrl', ResultsCtrl)