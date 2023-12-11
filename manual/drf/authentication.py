from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


# Возврат дополнительной информации о пользователе помимо token.
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

# Кастомная аутентификация любого входящего запроса как пользователя, 
# указанного в имени пользователя в заголовке X-USERNAME.
class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        # Если аутентификация прошла успешно должен возвращать кортеж (user, 
        # auth), иначе None.
        return (user, None)

    # Возвращает значение заголовка WWW-Authenticate в ответе HTTP 401 
    # Unauthorized.
    def authenticate_header(self, request):
        return super().authenticate_header(request)