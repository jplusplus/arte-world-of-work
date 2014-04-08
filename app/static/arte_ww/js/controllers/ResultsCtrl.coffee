_steps =
    intro : -1
    outro : -2

class ResultsCtrl
    @$inject: ['$scope', '$location', 'Thematic', '$http', '$sce', '$rootScope', "Xiti"]

    constructor: (@$scope, $location, @Thematic, @$http, @sce, @$rootScope, Xiti) ->       
        
        Xiti.loadPage("results")
        @elements = []

        # methods scope extending
        _.extend @$scope,
            filtered: @isFiltered
            filter: @filter
            start: @start 
            next: @next
            previous: @previous
            getTrustedHTML: @getTrustedHTML
            changeThematic: @changeThematic

        # attributes scope extending 
        _.extend @$scope,
            # List all thematics
            thematics: []

            hasNext: no
            hasPrev: no
            # handle current state (intro -> results -> (opt) outro)
            intro: 1

            current:
                thematic: 0
                answer:   0

            filters:
                age_min: 16
                age_max: 35
                male:   yes
                female: yes

        # watches
        @$scope.$watch (=>
            @Thematic.positionList
        ), @onThematicsLoaded

        @$scope.$watch 'current.thematic', (newValue, oldValue) =>
            if @$scope.thematics? and @$scope.thematics[@$scope.current.thematic]?
                @Thematic.onThematicPositionChanged @$scope.thematics[@$scope.current.thematic].position
        , yes

        @$scope.$watch =>
            @$scope.filters
        , @onFilterChanged, yes

        # Uncomment this block when you will want to enable deep linking
        # Update URL when the user changes filters
        # @$scope.$watch 'filters', (=>
        #     f = angular.copy @$scope.filters
        #     params = _.extend $location.search(),
        #         gender:  null
        #         age_min: f.age_min
        #         age_max: f.age_max

        #     if (f.male isnt f.female)
        #         params['gender'] = 'male' if f.male
        #         params['gender'] = 'female' if f.female

        #     $location.search params
        # ), yes

    getTrustedHTML: =>
        if @$scope.currentAnswer? and @$scope.currentAnswer.feedback?
            @sce.trustAsHtml @$scope.currentAnswer.feedback.html_sentence

    isFiltered: => 
        filters  = @$scope.filters
        filtered = filters.age_min != 16 or filters.age_max != 35
        filtered = filtered or not filters.male or not filters.female

    filter: (gender) =>
        filters = @$scope.filters
        if gender is 'female'
            if not filters.male and filters.female
                filters.male = yes 

        if gender is 'male'
            if not filters.female and filters.male
                filters.female = yes 

        @$scope.filters[gender] = not @$scope.filters[gender]

        if @$scope.filters.male is @$scope.filters.female is false
            @$scope.filters.male = @$scope.filters.female = true

    resetFilters: =>
        _.extend @$scope.filters,
            age_min: 16
            age_max: 35
            male:   yes
            female: yes

    changeThematic: (id) =>
        do @setThematicLoading
        for index of @$scope.thematics
            if @$scope.thematics[index].id is id
                @$scope.current.thematic = parseInt index
                @$scope.current.answer = 0
                if @elements[@$scope.current.thematic]?
                    @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
                    @$scope.intro = 0
                else
                    @$scope.intro = 1
                return

    retrieveCurrentResultsWithFilters: (id, callback=(=>)) =>
        request =
            url : "/api/questions/#{id}/results"
            method : 'GET'
            params :
                age_min : @$scope.filters.age_min
                age_max : @$scope.filters.age_max
        if @$scope.filters.male isnt @$scope.filters.female
            request.params.gender = 'male' if @$scope.filters.male
            request.params.gender = 'female' if @$scope.filters.female
        @$http(request).success (data) =>
            @setThematicLoaded =>
                do callback
                @$scope.currentAnswer = data
                do @setChartLoaded


    changeQuestion: (answer) =>
        current_thematic = @$scope.thematics[@$scope.current.thematic]
        if not (do @Thematic.current)?
            @Thematic.onThematicPositionChanged current_thematic.position, no
        @$scope.hasNext = @$scope.hasPrev = yes
        @$scope.nochart = false
        if answer.id >= 0
            @retrieveCurrentResultsWithFilters answer.id, =>
                if (do @Thematic.current).id isnt current_thematic.id
                    @Thematic.onThematicPositionChanged current_thematic.position, no 

            if @$scope.current.answer is 0
                @$scope.hasPrev = @elements[@$scope.current.thematic - 1]?
        else
            @setThematicLoaded =>
                @$scope.currentAnswer = answer
        @resetFilters()

    start: =>
        do @setThematicLoading
        @$scope.intro = 0
        if @elements[@$scope.current.thematic]?
            @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]
        else
            setTimeout (((o) => return => do o.$scope.start) @), 1000

    # Define Previous and Next behavior
    next: =>
        do @setThematicLoading
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
            @$scope.hasPrev = no

    previous: =>
        do @setThematicLoading
        if @$scope.intro is 2
            @$scope.intro = 0
        else
            if @elements[@$scope.current.thematic][@$scope.current.answer - 1]?
                --@$scope.current.answer
            else if @elements[@$scope.current.thematic - 1]?
                --@$scope.current.thematic
                @$scope.current.answer = @elements[@$scope.current.thematic].length - 1
        @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]


    onThematicsLoaded: =>
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
                        return _.filter thematic.elements, (t) -> t.type is 'question'
                        # elems = _.filter thematic.elements, (t) -> t.type is 'question'
                        # return elems.concat [{
                        #     content : thematic.outro_description
                        #     id : _steps.outro
                        #     label : thematic.title
                        # }]
                    else
                        return
                ), (e) -> e?
                if @$scope.intro == 0
                    @changeQuestion @elements[@$scope.current.thematic][@$scope.current.answer]

    

    setLoading: (state_name, loading=yes, fn) =>
        if @$scope[state_name] != loading
            @$rootScope.safeApply =>
                @$scope[state_name] = loading

        @$rootScope.safeApply fn 

    setThematicLoading: (fn) =>
        @setLoading 'isThematicLoading', yes, fn 

    setThematicLoaded: (fn) =>
        @setLoading 'isThematicLoading', no, fn 

    setChartLoading: (fn) =>
        @setLoading 'isChartLoading', yes, fn

    setChartLoaded: (fn) =>
        @setLoading 'isChartLoading', no, fn 

    onFilterChanged: =>
        if @$scope.currentAnswer? and @$scope.currentAnswer.id?
            do @setChartLoading
            @retrieveCurrentResultsWithFilters @$scope.currentAnswer.id


angular.module('arte-ww')
.controller('ResultsCtrl', ResultsCtrl)