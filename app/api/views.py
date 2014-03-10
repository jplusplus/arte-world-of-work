from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, link
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_countries import countries as django_countries
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
            serializer = serializers.QuestionResultsSerializer(question, 
                context={'request': request})
            return Response(serializer.data)

        except ObjectDoesNotExist:
            err = 'Given question with id `{id}` doesn\'t exist, thus results cannot be calculated'
            message = err.format(id=pk)
            return Response(message, 404)

    @link()
    def feedback(self, request, pk):
        try:
            question = self.queryset.get(pk=pk).as_final()
            serializer = serializers.QuestionFeedbackSerializer(question, 
                context={'request': request})
            return Response(serializer.data)

        except BaseQuestion.DoesNotExist:
            err_msg = (
                'Given question with id `{id}` doesn\'t exist, thus dynamic '
                'feedback cannot be calculated'
            )
            return Response(err_msg.format(id=pk), 404)

     

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
    permission_classes = (IsAuthenticated, IsOwner)

    def update_request(self, request):
        request.DATA.update({'user': request.user.pk})

    def create(self, request, *args, **kwargs):
        self.update_request(request)
        return super(AnswerViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.update_request(request)
        return super(AnswerViewSet, self).update(request, *args, **kwargs)

class CountryViewSet(viewsets.ViewSet):
    def list(self, request):
        # Pick the other countries        
        qs = [ c for c in django_countries.countries if c[0] not in ["FR", "DE"] ]        
        # Sort he list
        qs.sort(key=lambda x: x[0])        
        # Pick France and Germany
        qs = [ c for c in django_countries.countries if c[0] in ["FR", "DE"] ] + qs
        serializer = serializers.CountrySerializer(qs, many=True)
        return Response(serializer.data)

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

class VerifyToken(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)

verify_auth_token = VerifyToken.as_view()


class GPlusCount(APIView):
    def get(self, request):
        url = request.GET.get("url", None)

        if url is None:
            count = 0
        else:
            import urllib2, re
            
            usock = urllib2.urlopen('https://plusone.google.com/_/+1/fastbutton?url=%s' % url)
            xml = usock.read()
            usock.close()

            root = re.search('<div\s+id="aggregateCount".+>([ 0-9>a-zA-Z]+)</div>', xml)            
            count = root.group(1)
        
        return Response(status=status.HTTP_200_OK, data={'count': count})