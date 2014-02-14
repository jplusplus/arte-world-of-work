from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from app.api import serializers
from app.core.models import Thematic, UserPosition, BaseAnswer

# bind this `User` to current used User model (see `settings.AUTH_USER_MODEL`)
User = get_user_model()

# /results/
class InheritedModelCreateMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_final_serializer(data=request.DATA, files=request.FILES)
        # import pdb; pdb.set_trace()
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_final_serializer(self, data, files):
        base_serializer = self.get_serializer(data=data, files=files)
        assert isinstance(base_serializer, serializers.InherithedModelSerializerMixin) 
        return base_serializer.as_final_serializer(data=data, files=files)


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

class AnswerViewSet(viewsets.ModelViewSet, InheritedModelCreateMixin):
    """
    Endpoint for every answer actions
    @list():
        return all current user answers (can be saw as its parcour) 
    """
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return BaseAnswer.objects.user_answers(self.request.user.pk)

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




