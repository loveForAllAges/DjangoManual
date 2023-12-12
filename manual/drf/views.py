from rest_framework import (
    views, mixins, generics, authentication, permissions, viewsets, renderers,
)
from rest_framework.response import Response
from rest_framework.throttling import (
    UserRateThrottle
)
from rest_framework.metadata import SimpleMetadata
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import (
    api_view, throttle_classes, authentication_classes, permission_classes,
    schema, action, renderer_classes
)

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, PostSerializer, AlbumSerializer7
from .models import Post, Album
from .pagination import (
    StandardResultsSetPagination, CustomLimitOffsetPagination, 
    CustomCursorPagination, CustomPagination
)
from .throttling import (
    CustomAnonRateThrottle, CustomUserRateThrottle, CustomScopedRateThrottle,
    RandomRateThrottle
)

from django_filters.rest_framework import DjangoFilterBackend


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
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAdminUser])
@schema(CustomAutoSchema())
def api_view_func(request):
    ip = request.META['REMOTE_ADDR']
    return Response({'ip': ip})


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


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'object': self.object}, template_name='object.html')


@api_view(['GET'])
@renderer_classes([renderers.StaticHTMLRenderer])
def simple_html_view(request):
    data = '<h1>HEADER</h1>'
    return Response(data)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'body']
    throttle_classes = [OncePerDayUserThrottle]


class ThrottleAPIView(views.APIView):
    throttle_classes = [RandomRateThrottle]
    # throttle_scope = 'a'
    def get(self, request):
        return Response({'ok': 'ok'})


class CustomListAPIView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer7


@api_view(['GET'])
def me(request):
    return Response({
        'user': str(request.user),
        'auth': str(request.auth),
    })


class APIRoot(views.APIView):
    metadata_class = SimpleMetadata

    def get(self, request, format=None):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        return Response(data)
    

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