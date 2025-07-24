from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views


router_v1 = SimpleRouter()
router_v1.register(
    r'users',
    views.UsersViewSet,
    basename='users'
)
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
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='title-reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='title-review-comments'
)

auth_urls = [
    path(
        'token/',
        views.obtain_auth_token,
        name='get_token'
    ),
    path(
        'signup/',
        views.create_user_and_send_code,
        name='register'
    ),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls))
]
