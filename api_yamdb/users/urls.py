from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    r'users',
    views.UsersViewSet,
    basename='users'
)

urlpatterns = [
    path(
        'v1/auth/token/',
        views.UserObtainAuthToken.as_view(),
        name='get_token'
    ),
    path(
        'v1/auth/signup/',
        views.RegisterUserViewSet.as_view(),
        name='register'
    ),
    path('v1/', include(router_v1.urls)),
]
