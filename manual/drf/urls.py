from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'users2', UserModelViewSet, basename='user2')
# ИЛИ
# user_list = UserViewSet.as_view({'get': 'list'})
# user_detail = UserViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('me', me),
    path('views/', ListUsers.as_view()),
    path('api_view/', api_view_func),
    path('ListCreateAPIView/', UserList2.as_view()),
    path('ViewSet/', include(router.urls)),
    path('htmlrenderer/<int:pk>/', UserDetail.as_view()),
    path('statichtmlrenderer/', simple_html_view),
    path('posts', PostListAPIView.as_view()),
    path('throttle', ThrottleAPIView.as_view()),
    path('', APIRoot.as_view()),
    path('<int:pk>', CustomListAPIView.as_view(), name='album-detail'),
]
