from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, GroupViewSet, CommentViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='post-comments'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update',
                               'patch': 'partial_update', 'delete': 'destroy'}),
         name='post-comment-detail'),
]
