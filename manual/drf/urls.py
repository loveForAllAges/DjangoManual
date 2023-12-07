from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter

"""
PART 1 ListCreateAPIView
"""

# urlpatterns = [
#     path('tasks/', TasksAPIView.as_view()),
#     path('tasks/', TaskListCreateAPIView.as_view()),
#     path('tasks/', ListCreateAPIView.as_view(queryset=Task.objects.all(), serializer_class=TaskSerializer)),
# ]

"""
PART 2 GenericAPIView
"""

# urlpatterns = [
#     path('tasks/', TaskGenericAPIView.as_view()),
# ]

"""
PART 3 ListAPIView, 
"""

# urlpatterns = [
#     path('tasks/', TaskListAPIView.as_view()),
#     path('tasks/<int:pk>/', TaskDetailAPIView.as_view()),
# ]


"""
PART 4 Viewset, ModelViewset
"""

# router = DefaultRouter()
# router.register(r'tasks', TaskViewset, basename='task')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# router = DefaultRouter()
# router.register(r'tasks', TaskModelViewset, basename='task')
# router.register(r'track', TrackAPIView, basename='track')
# router.register(r'albums', AlbumAPIView, basename='album')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


urlpatterns = [
    # path('', test),
    # path('', include(router.urls)),
    # path('album', AlbumListAPI.as_view())
]


# from rest_framework.request import Request
# from rest_framework.response import Response