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
"""



# ========================



"""
rest_framework.status

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



1xx - Информационный (предварительный ответ. По умолчанию в DRF не используются)
2xx - Успешно (запрос клиента успешно получен, понят и принят)
3xx - Перенаправление (агенту пользователя необходимо предпринять дополнительные действия для выполнения запроса)
4xx - Ошибка клиента (клиент ошибся)
5xx - Ошибка сервера (сервер знает что он ошибся)

HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
HTTP_102_PROCESSING
HTTP_103_EARLY_HINTS
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS
HTTP_208_ALREADY_REPORTED
HTTP_226_IM_USED
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT
HTTP_308_PERMANENT_REDIRECT
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_421_MISDIRECTED_REQUEST
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_425_TOO_EARLY
HTTP_426_UPGRADE_REQUIRED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_506_VARIANT_ALSO_NEGOTIATES
HTTP_507_INSUFFICIENT_STORAGE
HTTP_508_LOOP_DETECTED
HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
HTTP_510_NOT_EXTENDED
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED

Определение кода ответа:
is_informational()  # 1xx
is_success()        # 2xx
is_redirect()       # 3xx
is_client_error()   # 4xx
is_server_error()   # 5xx
"""