from rest_framework import routers
from .views import ThematicViewSet, NestedThematicViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'thematics',        ThematicViewSet)
router.register(r'thematics-nested', NestedThematicViewSet, base_name='thematic-nested')
router.register(r'user',             UserViewSet, base_name='user')

urlpatterns = router.urls