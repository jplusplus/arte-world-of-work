from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from app.api import serializers
from app.core.models import Thematic, UserProfile
# /results/

# /survey/
class ThematicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint of survey. 
    
      - GET `/api/thematic/`
        
        > return a list of thematics and their survey elements (feedbacks + questions)
      
      - GET `/api/thematic/:id/`

        >  return the survey elements

    """

    queryset = Thematic.objects.all()
    serializer_class = serializers.ThematicSerializer


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

class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        user = User.objects.create(username='', password='')
        serializer = serializers.UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=['GET', 'PUT'])
    def mypostion(self, request):
        position = UserPosition.objects.get(user=request.user)
        serializer = serializers.UserPositionSerializer(position)
        return Response(data=serializer.data)




