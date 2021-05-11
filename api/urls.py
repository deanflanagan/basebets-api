from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import BlindAwayViewSet, ProfileViewSet, UserViewSet, GameViewSet, StrategyViewSet, SupporterViewSet

router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('games', GameViewSet)
router.register('strategies', StrategyViewSet)
router.register('profiles', ProfileViewSet)

router.register('supporter', SupporterViewSet, basename='supporter')
router.register('away', BlindAwayViewSet, basename='away')


urlpatterns = [
    path('', include(router.urls)),

    # path('authenticate', CustomObtainAuthToken.as_view())
]
