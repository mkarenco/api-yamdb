from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView)
from rest_framework.routers import DefaultRouter

from api.views import RegisterUserViewSet, UserProfileViewSet


router_v1 = routers.DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]


router_v1 = DefaultRouter()
router_v1.register(r'users', UserProfileViewSet, basename='users')


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/signup/', RegisterUserViewSet, name='register'),
    # path('users/<')
    path('me/', include(router_v1.urls)),


