from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', lambda request: JsonResponse({
        'message': 'Yatube API',
        'version': 'v1',
        'endpoints': {
            'posts': '/api/v1/posts/',
            'groups': '/api/v1/groups/',
            'follow': '/api/v1/follow/',
            'jwt': '/api/v1/jwt/',
            'documentation': '/redoc/'
        }
    }), name='api-root'),
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view(
             {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
              'delete': 'destroy'}),
         name='comment-detail'),
    path('v1/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
