from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    views.UsersViewSet,
    basename='users'
)

urlpatterns = [
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/',
        views.RegisterUserViewSet.as_view(),
        name='register'
    ),
    path('', include(router_v1.urls)),
]
