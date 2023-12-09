from rest_framework import (
    views, mixins, generics, authentication, permissions, viewsets
)
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import (
    api_view, throttle_classes, authentication_classes, permission_classes,
    schema, action
)

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer


class ListUsers(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'


class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        pass


@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
@schema(CustomAutoSchema())
def api_view_func(request):
    usernames = [user.username for user in User.objects.all()]
    return Response(usernames)


class UserList2(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        print(self.action)
        permission_classes = []
        # if self.action == 'list':
        #     permission_classes = []
        # else:
        #     permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def new_method(self, request):
        return Response({'content': 'test'})




"""
Пример документирования API:
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)


"""