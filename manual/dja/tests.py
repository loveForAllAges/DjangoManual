from .models import Animal
from django.test import Client, TestCase
import unittest


"""
Раздел: Testing in Django (Тестирование)


Модульные тесты используют unittest.
Тесты запускаются в режиме DEBUG=False.
Тесты не используют реальную БД, для них создается отдельные пустые БД.
После выполнения тестов тестовые БД удаляются.
test --keepdb - не удалять тестовую БД.
test --noinput - автоматическое удаление БД.
test --shuffle и --reverse - рандомный запуск тестов.
test --parallel - параллельное выполнение тестов.

Запуск тестов: python manage.py test
Запуск тестов по каталогу: python manage.py test animals/
Запуск тестов по имени файла: python manage.py test --pattern='tests_*.py'
"""


class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name='lion', sound='roar')
        Animal.objects.create(name='cat', sound='meow')
    
    def test_animals_can_speak(self):
        """
        Animals that can speak are correcty identified
        """
        lion = Animal.objects.get(name='lion')
        cat = Animal.objects.get(name='cat')
        self.assertEqual(lion.speak(), 'roar')
        self.assertEqual(cat.speak(), 'meow')


"""
Инструменты тестирования


Client(enforce_csrf_checks=False, raise_request_exception=True, json_encoder=DjangoJSONEncoder, *, headers=None, **defaults) - тестируемый HTTP-клиент.
Аргументы:
    - headers - заголовки по умолчанию, которые будут отправляться к каждым запросом. Например: Client(headers={'user-agent': 'curl/7.79.1'}).
    - **defaults - аргументы произвольного ключевого слова. Например: Client(SCRIPT_NAME='/app/').
    - enforce_csrf_checks - проверка защиты CSRF. По умолчанию False.
    - raise_request_exception - должны ли исключения вызываться в тесте. По умолчанию True.
    - json_decoder - кодировщик JSON для сериализации.
    - cookies - текущие значения всех cookie файлов.
    - session - информация о сеансе.
Методы:
    - get(path, data=None, follow=False, secure=False, *, headers=None, **extra) - выполняет GET запрос и возвращает Response (follow: следовать ли всем перенаправлениям; secure: эмулировать ли HTTPS-запрос).
    - post(path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, *, headers=None, **extra) - выполняет POST запрос и возвращает Response (content_type: тип контента).
    - head(path, data=None, follow=False, secure=False, *, headers=None, **extra) - выполняет HEAD запрос и возвращает Response. Работает также как get() но не возвращает тело сообщения.
    - options(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra) - выполняет запрос OPTIONS и возвращает Response. Полезно для RESTful-интерфейсов.
    - put(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra) - выполняет PUT запрос и возвращает Response.
    - patch(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra) - выполняет PATCH запрос и возвращает Response.
    - delete(path, data='', content_type='application/octet-stream', follow=False, secure=False, *, headers=None, **extra) - выполняет DELETE запрос и возвращает Response.
    - trace(path, follow=False, secure=False, *, headers=None, **extra) - выполняет TRACE запрос и возвращает Response.
    - login(**credentials) - имитация эффекта входа пользователя на сайт. После вызова клиент будет иметь все cookie авторизации.
    - force_login(user, backend=None) - имитация входа, замена login(), если не важно как пользователь вошел в систему.
    - logout() - имитация эффекта выхода пользователя из системы.

    
get() и post() возвращают Response != HttpResponse.

Response()
Атрибуты:
    - client - тестовый клиент, который использовался.
    - content - тело ответа в виде байтовой строки.
    - context - экземпляр шаблона Context.
    - exc_info - кортеж трех значений (type, value, traceback) с информацией об исключении.
    - json - тело ответа, анализируемое как JSON.
    - request - данные запроса.
    - wsgi_request - экземпляр WSGIRequest, который создал ответ.
    - status_code - статус HTTP ответа.
    - templates - список Template шаблонов для рендеринга содержимого.
    - resolver_match - экземпляр ResolverMatch для ответа.


>>> from django.test import Client
>>> c = Client()
>>> response = c.post('as', {'username': 'john', 'password': '123'})
>>> response = c.get('/as')
OK
"""

class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_details(self):
        response = self.client.get('/customer/details/')
        self.assertEqual(response.status_code, 200)


        self.assertEqual(len(response.context['customers']), 5)


"""
-- SimpleTestCase


Наследует unittest.TestCase.

Атрибуты:
    - databases - '__all__', если нужно записывать в БД. По умолчанию запросы к БД запрещены.


-- TransactionTestCase


Наследует SimpleTestCase.

Сбрасывает БД в известное состояние в начале каждого теста. БД fixtures. 


-- TestCase


Наследуется от TransactionTestCase.
Самый распространенный для написания тестов.

Методы:
    - setUpTestData() - позволяет проводить более быстрые тесты по сравнению с setUp().
    - captureOnCommitCallbacks(using=DEFAULT_DB_ALIAS, execute=False) - возвращает список, который содержит захваченные функции обратного вызова (using: псевдоним соединения с БД; execute: вызывать ли обратные вызовы при выходе из контекста).
"""

from django.core import mail


class MyTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Foo = 'Model'
        cls.foo = Foo.objects.create(bar='Test')
        return super().setUpTestData()
    
    def test1(self):
        return
    
    def test2(self):
        return

    def test_post(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(
                '/contact/', {'message': 'message'}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox[0].subject), 'Form')
        self.assertEqual(mail.outbox[0].body, 'body')


"""
-- LiveServerTestCase


LiveServerTestCase по сути делает то же самое, что TransactionTestCase с одной дополнительной функцией: 
он запускает работающий сервер Django в фоновом режиме при настройке и выключает его при отключении. 
Это позволяет использовать клиенты автоматического тестирования, отличные от фиктивного клиента Django , такие как, например, клиент Selenium , для выполнения серии функциональных тестов внутри браузера и имитации действий реального пользователя.


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["user-data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("secret")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
"""


"""
Подробнее:
https://docs.djangoproject.com/en/4.2/topics/testing/tools/
https://docs.djangoproject.com/en/4.2/topics/testing/advanced/
"""