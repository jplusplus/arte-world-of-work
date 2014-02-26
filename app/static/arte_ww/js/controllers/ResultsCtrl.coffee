class ResultsCtrl
    @$inject: ['$scope', '$location', 'Thematic']

    constructor: ($scope, $location, Thematic) ->
        # Update URL when the user changes filters
        $scope.$watch 'filters', (=>
            f = angular.copy $scope.filters
            $location.search 'gender', null
            if (f.male isnt f.female)
                ($location.search 'gender', 'male') if f.male
                ($location.search 'gender', 'female') if f.female
            $location.search 'age_min', f.age_min
            $location.search 'age_max', f.age_max
        ), yes

        $scope.thematics = []
        $scope.$watch (=>
            Thematic.positionList
        ), =>
            if Thematic.positionList?
                $scope.thematics = _.map Thematic.positionList.elements, (thematic) =>
                    slug : thematic.slug
                    title : thematic.title

        # Initialize filters (fron URL or default values)
        urlFilters = do $location.search
        $scope.filters =
            age_min : urlFilters.age_min or 0
            age_max : urlFilters.age_max or 99
            male : if urlFilters.gender isnt 'female' then yes else no
            female : if urlFilters.gender isnt 'male' then yes else no

        # Make sure we can't deselect both genders
        $scope.filter = (gender) =>
            $scope.filters[gender] = not $scope.filters[gender]
            if $scope.filters.male is $scope.filters.female is false
                $scope.filters.male = $scope.filters.female = true

angular.module('arte-ww')
.controller('ResultsCtrl', ResultsCtrl)