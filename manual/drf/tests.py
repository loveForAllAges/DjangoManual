"""
rest_framework.test



APIRequestFactory()
Расширяет RequestFactory() от Django. Поддерживает почти такой же API, как и стандартный класс.
Доступные методы: get, post, put, patch, delete, head, options.

from rest_framework.test import APIRequestFactory
factory = APIRequestFactoty()
request = factory.post('/notes/', {'title': 'new title'})

Методы, содержащие тело запроса, такие как post, put, patch, включают аргумент format, что облегчает генерацию запросов, использующих тип содержимого, отличный от многокомпонентных данных формы. Например:
request = factory.post('/notes/', {'title': 'new idea'}, format='json')

По умолчанию доступны форматы multipart и json. По умолчанию используется multipart.

Явное кодирование тела запроса:
request = factory.post('/notes/', json.dumps({'title': 'new_title'}), content_type='application/json')

Принудительная аутентификация
from rest_framework.test import force_authenticate
factory = APIRequestFactory()
user = User.objects.get(username='olivia')
view = AccountDetail.as_view()
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
response = view(request)

Принудительная аутентификация с помощью токена:
user = User.objects.get(username='olivia')
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user, token=user.auth_token)

Принудительная проверка CSRF
По умолчанию запросы, созданные с помощью APIRequestFactory, не будут проходить проверку CSRF при передаче в представление DRF. Если вам необходимо явно включить проверку CSRF, вы можете сделать это, установив флаг enforce_csrf_checks при инстанцировании фабрики.
factory = APIRequestFactory(enforce_csrf_checks=True)



APIClient()
Расширяет существующий класс Client.
Поддерживает методы: get, post, put, patch, delete, head, options.

from rest_framework.test import APIClient
client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')

Аутентификация
.login(**kwargs)
Работает также как и в Client(). Позволяет аутентифицировать запрос к любым представлениям, которые включают SessionAuthentication.

client = APIClient()
client.login(username='lauren', password='secret')
client.logout()

Метод login подходит для тестирования API, использующих сеансовую аутентификацию, например, веб-сайтов, включающих AJAX-взаимодействие с API.

.credentials(**kwargs)
Можно использовать для установки заголовков, которые затем будут включены во все последующие запросы.
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
token = Token.objects.get(user__username='lauren')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

Вызов credentials перезаписывает все существующие учетные данные.
Чтобы очистить: client.credentials().

Метод credentials подходит для тестирования API, требующих заголовков аутентификации, таких как базовая аутентификация, аутентификация OAuth1a и OAuth2, а также простые схемы аутентификации токенов.

.force_authenticate(user=None, token=None)
Позволяет полностью обойти аутентификацию и заставить все запросы тестового клиента рассматриваться как аутентифицированные.
user = User.objects.get(username='lauren')
client = APIClient()
client.force_authenticate(user=user)

Чтобы не аутентифицировать последующие запросы, необходимо вызвать: client.force_authenticate(user=None)

Проверка CSRF
По умолчанию не применяется, чтобы включить:
client = APIClient(enforce_csrf_checks=True)
Обычно, проверка будет применяться только к аутентифицированным пользователям.



RequestsClient()
DRF включает клиент для взаимодействия с помощью requests.

Это предоставляет точно такой же интерфейс, как если бы вы использовали сессию запросов напрямую.
from rest_framework.test import RequestsClient
client = RequestsClient()
response = client.get('http://testserver/users/')
assert response.status_code == 200

Пользовательские заголовки и учетные данные аутентификации могут быть предоставлены также, как и при использовании requests.Session.
from requests.auth import HTTPBasicAuth
client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})

Если используется SessionAuthentication, то необходимо включить CSRF-токен для запросов post, put, patch, delete.

Получить токен можно так:
client = RequestsClient()
response = client.get('http://testserver/homepage/')
assert response.status_code == 200
csrftoken = response.cookies['csrftoken']
response = client.post('http://testserver/organisations/', json={
    'name': 'MegaCorp',
    'status': 'active'
}, headers={'X-CSRFToken': csrftoken})
assert response.status_code == 200



CoreAPIClient()
Позволяет взаимодействовать с API с помощью клиентской библиотеки Python coreapi.

client = CoreAPIClient()
schema = client.get('http://testserver/schema/')
params = {'name': 'MegaCorp', 'status': 'active'}
client.action(schema, ['organisations', 'create'], params)
data = client.action(schema, ['organisations', 'list'])
assert(len(data) == 1)
assert(data == [{'name': 'MegaCorp', 'status': 'active'}])

Пользовательские заголовки и аутентификации могут использоваться с CoreAPIClient как и с RequestsClient.

from requests.auth import HTTPBasicAuth
client = CoreAPIClient()
client.session.auth = HTTPBasicAuth('user', 'pass')
client.session.headers.update({'x-test': 'true'})



Тесты API
DRF включает следующие классы тестов, которые являются зеркальным отражением существующих Django's test case classes, но используют APIClient вместо Django's default Client.
- APISimpleTestCase.
- APITransactionTestCase
- APITestCase
- APILiveServerTestCase


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myproject.apps.core.models import Account

class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')



URLPatternsTestCase()
DRF также предоставляет класс тестов для изоляции urlpatterns на основе каждого класса. Обратите внимание, что он наследуется от Django SimpleTestCase, и, скорее всего, его придется смешивать с другим классом тестов.

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_create_account(self):
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        
        
При проверке достоверности тестовых ответов часто удобнее проверять данные, на основе которых был создан ответ, чем проверять полностью отрисованный ответ.
Например, проще проверить response.data:
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})

Вместо того чтобы проверять результат разбора response.content:
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})


"""
