from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from app.api import serializers, mixins
from app.api.permissions import IsOwner
from app.core.models import Thematic, UserPosition, BaseAnswer

# bind this `User` to current used User model (see `settings.AUTH_USER_MODEL`)
User = get_user_model()


class NestedThematicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint of survey.
    
      - GET `/api/thematic-nested/`
        
        > return a list of thematics and their survey elements (feedbacks + questions)
      
      - GET `/api/thematic-nested/:id/`

        >  return the survey elements

    """
    queryset = Thematic.objects.all()
    serializer_class = serializers.NestedThematicSerializer


class ThematicResultsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Thematic.objects.all()
    serializer_class = serializers.ThematicResultsSerializer

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

class MyAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = BaseAnswer.objects.all()

    def get_queryset(self):
        return super(MyAnswerViewSet, self).get_queryset().filter(user=self.request.user.pk)

class AnswerViewSet(viewsets.ModelViewSet, mixins.InheritedModelCreateMixin):
    """
    Endpoint for every answer actions
    @list():
        return all current user answers (can be saw as its parcour) 
    """
    queryset = BaseAnswer.objects.all()
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.DATA.update({'user': request.user.pk})
        return super(AnswerViewSet, self).create(request, *args, **kwargs)

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

