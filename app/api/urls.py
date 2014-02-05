from rest_framework import routers
from .views import SurveyViewSet

router = routers.SimpleRouter()
router.register(r'survey', SurveyViewSet, base_name='survey')

urlpatterns = router.urls