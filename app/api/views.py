from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from app.core.models import Thematic, UserPosition, BaseAnswer, BaseQuestion
from app.api import serializers, mixins
from app.api.permissions import IsOwner

# bind this `User` to current used User model (see `settings.AUTH_USER_MODEL`)
User = get_user_model()

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BaseQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer

    @link()
    def results(self, request, pk):
        try:
            question = self.queryset.get(pk=pk).as_final()
        except ObjectDoesNotExist:
            err = 'Given question with id `{id}` doesn\'t exist, thus results cannot be calculated'
            message = err.format(id=pk)
            return Response(message, 404)

        serializer = serializers.QuestionResultsSerializer(question, context={'request': request})
        return Response(serializer.data)

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
    def list(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True, 
            context={'request': request})
        return Response(serializer.data)

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

class AnswerViewSet(viewsets.ModelViewSet, 
                    mixins.CreateInheritedModelMixin,
                    mixins.UpdateInheritedModelMixin):
    """
    Endpoint for every answer actions
    @list():
        return all current user answers (can be saw as its parcour) 
    """
    queryset = BaseAnswer.objects.all()
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
 
    read_only_fields = ('user',)
    exclude = ('content_type')
    def update_request(self, request):
        request.DATA.update({'user': request.user.pk})

    def create(self, request, *args, **kwargs):
        self.update_request(request)
        return super(AnswerViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.update_request(request)
        return super(AnswerViewSet, self).update(request, *args, **kwargs)

class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        user = User.objects.create()
        serializer = serializers.UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class MyPositionView(generics.RetrieveUpdateAPIView):
    model = UserPosition
    serializer_class = serializers.UserPositionSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.userposition