_steps =
    intro : -1
    outro : -2

class ResultsCtrl
    @$inject: ['$scope', '$location', 'Thematic', '$http', '$sce', '$rootScope', "Xiti"]

    changeQuestion: (id) =>
        @$rootScope.isThematicLoading = yes
        if not (do @Thematic.current)?
            @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
        @$scope.hasNext = @$scope.hasPrev = yes
        @$scope.nochart = true
        if id.id >= 0
            request =
                url : "/api/questions/#{id.id}"
                method : 'GET'
            @$http(request).success (data) =>
                if (do @Thematic.current).id isnt @$scope.thematics[@$scope.current.thematic].id
                    @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
                @$scope.currentAnswer = data
            if @$scope.current.answer is 0
                @$scope.hasPrev = @elements[@$scope.current.thematic - 1]?
        else
            @$rootScope.isThematicLoading = no
            @$scope.currentAnswer = id

    constructor: (@$scope, $location, @Thematic, @$http, $sce, @$rootScope, Xiti) ->       
    
        Xiti.loadPage("results")

        # Update URL when the user changes filters
        @$scope.$watch 'filters', (=>
            f = angular.copy @$scope.filters
            params = _.extend $location.search(),
                gender:  null
                age_min: f.age_min
                age_max: f.age_max

            if (f.male isnt f.female)
                params['gender'] = 'male' if f.male
                params['gender'] = 'female' if f.female

            $location.search params
        ), yes

        @$scope.filtered = =>
            if ((parseInt @$scope.filters.age_min) is 16) and ((parseInt @$scope.filters.age_max) is 35) and @$scope.filters.male and @$scope.filters.female
                no
            else
                yes

        @$scope.hasNext = no
        @$scope.hasPrev = no
        @$scope.intro = 1

        @$scope.current =
            thematic : 0
            answer : 0

        @$scope.getTrustedHTML = =>
            if @$scope.currentAnswer? and @$scope.currentAnswer.feedback?
                $sce.trustAsHtml @$scope.currentAnswer.feedback.html_sentence

        @$scope.start = =>
            @$scope.intro = 0
            if @elements[@$scope.current.thematic]?
                @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
            else
                setTimeout (((o) => return => do o.$scope.start) @), 1000

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
                            elems = _.filter thematic.elements, (t) -> t.type is 'question'
                            return elems.concat [{
                                content : thematic.outro_description
                                id : _steps.outro
                                label : thematic.title
                            }]
                        else
                            return
                    ), (e) -> e?
                    if @$scope.intro == 0
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
                @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
            else if @elements[@$scope.current.thematic + 1]?
                ++@$scope.current.thematic
                @$scope.current.answer = 0
                @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
            else
                @$scope.intro = 2
                @$scope.hasNext = no
                @$scope.hasPrev = yes

        @$scope.previous = =>
            if @$scope.intro is 2
                @$scope.intro = 0
            else
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
                    if @elements[@$scope.current.thematic]?
                        @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
                    @$scope.intro = 0
                    return

        @$scope.$watch 'current.thematic', (newValue, oldValue) =>
            if @$scope.thematics? and @$scope.thematics[@$scope.current.thematic]?
                @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
        , yes

angular.module('arte-ww')
.controller('ResultsCtrl', ResultsCtrl)