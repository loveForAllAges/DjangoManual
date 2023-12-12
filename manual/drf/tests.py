from django.urls import reverse, include, path
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import (
    APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate,
    APIClient, RequestsClient, CoreAPIClient
)
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth

from .views import me

import json


def APIRequestFactory_test():
    factory = APIRequestFactory()
    request = factory.post('/notes/', {'title': 'new title'})
    # Явное кодирование тела запроса
    request = factory.post(
        '/notes/', 
        json.dumps({'title': 'new idea'}), 
        content_type='application/json'
    )

    # Принудительная аутентификация
    user = User.objects.get(username='olivia')
    view = me
    request = factory.get('/accounts/django-superstars/')
    force_authenticate(request, user=user)
    response = view(request)

    # Принудительная аутентификация с помощью токена
    user = User.objects.get(username='olivia')
    request = factory.get('/accounts/django-superstars/')
    force_authenticate(request, user=user, token=user.auth_token)

    # Принудительная проверка CSRF
    factory = APIRequestFactory(enforce_csrf_checks=True)

    return


def APIClient_test():
    client = APIClient()
    client.post('/notes/', {'title': 'new idea'}, format='json')

    # Аутентификация пользователя
    client = APIClient()
    client.login(username='lauren', password='secret')
    client.logout()

    # Установка загловков
    token = Token.objects.get(user__username='lauren')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Обход аутентификации. Запросы будут рассматриваться как 
    # аутентифицированные.
    user = User.objects.get(username='lauren')
    client = APIClient()
    client.force_authenticate(user=user)

    # Включение проверки CSRF
    client = APIClient(enforce_csrf_checks=True)
    return


def RequestsClient_test():
    client = RequestsClient()
    response = client.get('http://testserver/users/')
    assert response.status_code == 200

    # Установка пользовательских заголовков и данных аутентификации.
    client.auth = HTTPBasicAuth('user', 'pass')
    client.headers.update({'x-test': 'true'})

    # Получение csrf для post запроса.
    client = RequestsClient()
    response = client.get('http://testserver/homepage/')
    assert response.status_code == 200
    csrftoken = response.cookies['csrftoken']
    response = client.post('http://testserver/organisations/', json={
        'name': 'MegaCorp',
        'status': 'active'
    }, headers={'X-CSRFToken': csrftoken})
    assert response.status_code == 200

    return


def CoreAPIClient_test():
    client = CoreAPIClient()
    schema = client.get('http://testserver/schema/')
    params = {'name': 'MegaCorp', 'status': 'active'}
    client.action(schema, ['organisations', 'create'], params)
    data = client.action(schema, ['organisations', 'list'])
    assert(len(data) == 1)
    assert(data == [{'name': 'MegaCorp', 'status': 'active'}])

    # Пользовательские заголовки
    client = CoreAPIClient()
    client.session.auth = HTTPBasicAuth('user', 'pass')
    client.session.headers.update({'x-test': 'true'})

    return


# Можно использовать любой из классов тестов.
class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'DabApps')



class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_create_account(self):
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
