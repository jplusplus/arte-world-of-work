from rest_framework import viewsets

from app.api import serializers
from app.core.models import Thematic
# /results/

# /survey/
class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Base viewset for Arte-WoW survey
    @list():
        return the list of all thematic and their respective
        questions + feedback
    """ 
    queryset = Thematic.objects.all_elements()
    serializer_class = serializers.SurveySerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Endpoint for every answer actions
    @list():
        return all current user answers (can be saw as its parcour) 
    """ 