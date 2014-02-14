from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from app.api import serializers
from app.core.models import Thematic, UserPosition, BaseAnswer

# get user model 
User = get_user_model()

# /results/

# /survey/
class NestedThematicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint of survey. 
    
      - GET `/api/thematic/`
        
        > return a list of thematics and their survey elements (feedbacks + questions)
      
      - GET `/api/thematic/:id/`

        >  return the survey elements

    """
    queryset = Thematic.objects.all()
    serializer_class = serializers.NestedThematicSerializer

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
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        request = self.request
        answers = BaseAnswer.objects.user_answers(request.user.pk)
        return answers


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        user = User.objects.create()
        serializer = serializers.UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(methods=['GET', 'PUT'])
    def mypostion(self, request, pk):
        position = UserPosition.objects.get(user=pk)
        serializer = serializers.UserPositionSerializer(position)
        return Response(data=serializer.data)




