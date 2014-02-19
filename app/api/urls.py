from rest_framework import routers
from app.api.viewsets import QuestionViewSet
from app.api.viewsets import ThematicViewSet
from app.api.viewsets import ThematicResultsViewSet
from app.api.viewsets import NestedThematicViewSet
from app.api.viewsets import UserViewSet
from app.api.viewsets import AnswerViewSet
from app.api.viewsets import MyAnswerViewSet

router = routers.DefaultRouter()
router.register(r'questions',        QuestionViewSet)
router.register(r'thematics',        ThematicViewSet)
router.register(r'thematics-nested', NestedThematicViewSet,  base_name='thematic-nested')
router.register(r'thematics-result', ThematicResultsViewSet, base_name='thematic-results')
router.register(r'user',             UserViewSet,            base_name='user')
router.register(r'answers',          AnswerViewSet,          base_name='answer')
router.register(r'my-answers',       MyAnswerViewSet,        base_name='my-answers')

urlpatterns = router.urls