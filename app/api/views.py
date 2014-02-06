from rest_framework import viewsets

from app.api import serializers
from app.core.models import Thematic
# /results/

# /survey/
class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint of survey. 
    
      - GET `/api/survey/`
        
        > return a list of thematics and their survey elements (feedbacks + questions)
      
      - GET `/api/survey/:id/`

        >  return the survey elements

    """

    queryset = Thematic.objects.all()
    serializer_class = serializers.SurveySerializer


class FeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for dynamic feedback. 

    Generate on demand dynamic feedback objects.
    """


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Endpoint for every answer actions
    @list():
        return all current user answers (can be saw as its parcour) 
    """ 
    # queryset = BaseAnswer.objects.all()
