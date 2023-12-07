"""
rest_framework.exceptions

Обрабатываемые исключения:
- APIException
- Http404
- PermissionDenied

Ошибки валидации возвращаются в виде словаря, где ключ это название поля, а значение - текст ошибки.
Если валидация не относится к полю, то ключ будет - non_field_errors. Можно поменять на другое в настройках параметром NON_FIELD_ERRORS_KEY.

Пример:
`
{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
`

APIEcxeption()
базовый класс для всех исключений, возникающих внутри класса APIView или @api_view.
Чтобы предоставить пользовательское исключение, подкласс APIException и установите атрибуты .status_code, .default_detail и .default_code для класса.
`
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
`



ParseError()
Возникает, если запрос содержит неправильно сформированные данные при доступе к request.data.
Ошибка: 400


AuthenticationFailed()
Возникает, когда входящий запрос содержит неправильную аутентификацию.
Ошибка: 401 или 403



NotAuthenticated()
Возникает, когда неаутентифицированные запрос не прошел проверку.
Ошибка: 401 или 403



PermissionDenied()
Возникает, когда неаутентифицированный запрос не прошел проверку на разрешение.
Ошибка: 403



NotFound()
Возникает, когда ресурс не существует по указанному URL. Эквивалентно Http404.
Ошибка: 404



MethodNotAllowed()
Возникает когда происходит входящий запрос, который не сопоставлен с методом-обработчиком на представлении.
Ошибка: 405



NotAcceptable()
Возникает, когда поступает запрос с заголовком Accept, который не может быть удовлетворен ни одним из доступных рендереров.
Ошибка: 406



UnsupportedMediaType()
Возникает, если при обращении к request.data нет парсеров, способных обработать тип содержимого данных запроса.
Ошибка: 415



Throttled()
Возникает, когда входящий запрос не проходит проверку на дросселирование.
Ошибка: 429



ValidationError(detail: List | Dict, code)
Используется для сериализатора и валидации полей. Также вызывается при serializer.is_valid(raise_exception=True).
Ошибка: 400



Общие представления об ошибках
rest_framework.exceptions.server_error
Возвращает ответ с кодом состояния 500 и типом содержимого application/json.
handler500 = 'rest_framework.exceptions.server_error'

rest_framework.exceptions.bad_request
Возвращает ответ с кодом статуса 400 и типом содержимого application/json.
handler400 = 'rest_framework.exceptions.bad_request'


Модуль включает набор вспомогательных функций для проверки того, находится ли код состояния в заданном диапазоне
`
from rest_framework import status
from rest_framework.test import APITestCase

class ExampleTestCase(APITestCase):
    def test_url_root(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
`
"""
