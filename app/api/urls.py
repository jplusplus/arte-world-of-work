from rest_framework import routers
from .views import ThematicViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'thematics', ThematicViewSet)
router.register(r'user',      UserViewSet, base_name='user')


urlpatterns = router.urls