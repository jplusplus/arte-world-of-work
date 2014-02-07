
describe 'arte-ww.ThematicCtrl', ->
    ctrl = scope = null 
    fake_survey =
        all: (cb)->
            cb([{"id": 1, "title": "You", "elements": [{"id": 1, "label": "What is your age ?", "hint_text": "Enter your age and validate", "content_type": 32, "skip_button_label": "Skip this question", "validate_button_label": "Done", "typology": "UserAgeQuestion", "answer_type": "UserAgeAnswer", "position": 0, "type": "question"}, {"id": 3, "label": "Where do you live ?", "skip_button_label": "Skip this question", "typology": "UserCountryQuestion", "answer_type": "UserCountryAnswer", "position": 1, "type": "question"}, {"id": 9, "label": "What is your gender ?", "skip_button_label": "Skip this question", "typology": "UserGenderQuestion", "answer_type": "UserGenderAnswer", "position": 2, "type": "question"}, {"id": 2, "label": "Where do you come from ?", "skip_button_label": "Skip this question", "typology": "UserCountryQuestion", "answer_type": "UserCountryAnswer", "position": 3, "type": "question"}], "intro_description": "Introduction", "intro_button_label": ""}, {"id": 2, "title": "Your work", "elements": [{"id": 10, "label": "Some say hey, other say ?", "skip_button_label": "Skip this question", "typology": "TextRadioQuestion", "answer_type": "RadioAnswer", "position": 0, "type": "question"}, {"id": 8, "label": "Do you agree with these statements ? ", "skip_button_label": "Skip this question", "typology": "TextSelectionQuestion", "answer_type": "SelectionAnswer", "position": 1, "type": "question"}, {"id": 7, "label": "What would be your perfect salary", "skip_button_label": "Skip this question", "typology": "TypedNumberQuestion", "answer_type": "TypedNumberAnswer", "position": 2, "type": "question"}, {"id": 6, "label": "Who is your boss ?", "skip_button_label": "Skip this question", "typology": "MediaRadioQuestion", "answer_type": "RadioAnswer", "position": 3, "type": "question"}, {"id": 5, "label": "My label is sexy", "skip_button_label": "Skip this question", "typology": "MediaSelectionQuestion", "answer_type": "SelectionAnswer", "position": 4, "type": "question"}, {"basechoicefield_set": [{"id": 1, "question": 4, "title": "yes"}, {"id": 2, "question": 4, "title": "no"}], "typology": "BooleanQuestion", "answer_type": "RadioAnswer", "position": 5, "type": "question", "id": 4}], "intro_description": "Serious business", "intro_button_label": "See the data"}])
    # load main module
    beforeEach module('arte-ww')

    beforeEach(inject(
        ($injector, $rootScope, $controller)->
            scope = $rootScope.$new()
            ctrl =  $controller('ThematicCtrl', {$scope: scope, 'Survey': fake_survey})
    ))

    it 'should have initialized scope variables', ->
        # currentPosition should be 0 
        expect(ctrl.scope.currentElementPosition).toBe 0

        # currentThematicPosition should be 0 
        expect(ctrl.scope.currentThematicPosition).toBe 0

    it 'should set outro to true on last element', -> 
        ctrl.scope.currentThematicPosition += 1
        ctrl.previous()

        expect(ctrl.scope.outro).toBe true 



            
