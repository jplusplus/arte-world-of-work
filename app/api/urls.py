from rest_framework import routers
from .views import ThematicViewSet, NestedThematicViewSet, UserViewSet, AnswerViewSet

router = routers.SimpleRouter()
router.register(r'thematics',        ThematicViewSet)
router.register(r'thematics-nested', NestedThematicViewSet, base_name='thematic-nested')
router.register(r'user',             UserViewSet, base_name='user')
router.register(r'answers',          AnswerViewSet, base_name='answer')

urlpatterns = router.urls