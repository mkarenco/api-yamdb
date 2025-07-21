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
        views.obtain_auth_token,
        name='get_token'
    ),
    path(
        'v1/auth/signup/',
        views.register_user,
        name='register'
    ),
    path('v1/', include(router_v1.urls)),
]
