from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

from . import views


router_v1 = routers.DefaultRouter()
router_v1.register(
    'titles',
    views.TitleViewSet,
    basename='title'
)
router_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='category'
)
router_v1.register(
    'genres',
    views.GenreViewSet,
    basename='genre'
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',  # Ищет title по ID
    views.ReviewsViewSet,
    basename='title-reviews'
)
# перенести в приложение Users
router_v1.register(
    r'users',
    views.UsersViewSet,
    basename='users'
)

urlpatterns = [
    path(
        'v1/',
        include(router_v1.urls)
    ),
    # перенести в приложение Users
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/',
        views.RegisterUserViewSet,
        name='register'
    ),
    path(
        'users/',
        include(router_v1.urls)
    ),
]
