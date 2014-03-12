from django.conf.urls import patterns, include, url
from rest_framework import routers

from app.api import views


router = routers.DefaultRouter()

router.register(r'thematics',        views.ThematicViewSet)
router.register(r'questions',        views.QuestionViewSet,        base_name='question')
router.register(r'thematics-nested', views.NestedThematicViewSet,  base_name='thematic-nested')
router.register(r'thematics-result', views.ThematicResultsViewSet, base_name='thematic-results')
router.register(r'countries',        views.CountryViewSet,         base_name='country')
router.register(r'user',             views.UserViewSet,            base_name='user')
router.register(r'my-answers',       views.MyAnswerViewSet,        base_name='my-answers')
router.register(r'answers',          views.AnswerViewSet,          base_name='answer')

urlpatterns = patterns('',
    url(r'^my-position/',  views.MyPositionView.as_view(), name='my-position'),
    url(r'^gplus-count/',  views.GPlusCount.as_view(), name='gplus-count'),
    url(r'^verify-token/', 'app.api.views.verify_auth_token', name='verify-token'),
)
urlpatterns += router.urls


