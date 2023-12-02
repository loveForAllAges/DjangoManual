
"""
from django.contrib.sessions.backends.db import SessionStore


Сессии могут храниться в БД, в кэше, в файловой системе.
По умолчанию сессии хранятся в БД django.contrib.sessions.models.Session.


Хранение сессий в кэше повышает производительность. Следует использовать в том случае, если серверая часть кэша Memcached или Redis.
Серверная часть кэша в локальной памяти долго не хранит данные.

Чтобы использовать другой кэш, необходимо установить имя кэша в SESSION_CACHE_ALIAS.
После настройки кэша нужно выбрать между кэшем на базе базы данных или непостоянным кэшем.

Серверная часть кэшированной БД (cached_db) использует кеш со сковзной записью (записи сеанса применяются как к кешу, так и к БД).
При чтении сеанса используется кэш или БД, если данные были удалены из кэша.
Чтобы использваоть этот бэкенд SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db' + следовать инструкциям по настройке.

Чтобы хранить данные сеанса только в кэше, необходимо установить в SESSION_ENGINE 'django.contrib.sessions.backends.cache'.
Но, если кэш будет удален, то все данные сессий удалятся.

Серверную часть кэша можно сделать постоянной, используя постоянный кэш, например, Redis.


Чтобы использовать сессии на основе файлов, необходимо установить в SESSION_ENGINE 'django.contrib.sessions.backends.file'.


Чтобы использовать сессии на основе файлов куки, необходимо установить в SESSION_ENGINE 'django.contrib.sessions.backends.signed_cookies'.
Данные будут храниться с использованием инструментов криптографической подписи и SECRET_KEY.

Рекомендуется оставить SESSION_COOKIE_HTTPONLY=True, чтобы предотвратить доступ к сохраненным данным из js.


SessionBase - базовый класс для всех обьектов сеанса.

Методы:
    - __getitem__(key) - пример request.session['fav_color']
    - __setitem__(key, value) - пример request.session['fav_color'] = 'blue'
    - __delitem__(key) - пример del request.session['fav_color]
    - __contains__(key) - пример 'fav_color' in request.session
    - get(key, default=None) - пример fav_color = reqeust.session.get('fav_color', 'red')
    - pop(key, default=__not_given) - пример fav_color = request.session.pop('fav_color', 'blue')
    - keys()
    - items()
    - setdefault()
    - clear()
    - flush() - удаляет текущие данные сеанса из сеанса и удаляет файл cookie сеанса.
    - set_test_cookie() - устанавливает тестовый файл cookie, чтобы определить, поддерживает ли браузер пользователя файлы cookie.
    - test_cookie_worked() - принял ли браузер пользователя тестовый файл cookie.
    - delete_test_cookie() - удаляет тестовый файл cookie.
    - get_session_cookie_age() - возвращает значение SESSION_COOKIE_AGE.
    - set_expiry(value) - устанавливает срок дейсвия сеанса.
    - get_expiry_age() - возвращает кол-во секунд до истечения срока действия этого сеанса.
    - get_expiry_date() - возвращает дату истечения срока действия сеанса.
    - get_expire_at_browser_close() - истечет ли срок действия файла cookie при закрытии браузера пользователя. 
    - clear_expired() - удаляет просроченные сеансы из хранилища сеансов. Метод класс называется clearsessions.
    - cycle_key() - создает новый ключ сеанса, сохраняя текущие данные сеанса.

    
SESSION_SAVE_EVERY_REQUEST=True - сохранение сеанса при каждом запросе, файл cookie будет отправляться при каждом запросе.    
SESSION_EXPIRE_AT_BROWSER_CLOSE=True - сессии пока не будет закрыт браузер. По умолчанию False, сессии живут SESSION_COOKIE_AGE.


Таблица сессий не накапливает устаревшие сессии. Чтобы их очистить - clearsessions.


Настройки сессий:
1. SESSION_CACHE_ALIAS
2. SESSION_COOKIE_AGE
3. SESSION_COOKIE_DOMAIN
4. SESSION_COOKIE_HTTPONLY
5. SESSION_COOKIE_NAME
6. SESSION_COOKIE_PATH
7. SESSION_SAMESITE
8. SESSION_SECURE
9. SESSION_ENGINE
10. SESSION_EXPIRE_AT_BROWSER_CLOSE
11. SESSION_FILE_PATH
12. SESSION_SAVE_EVERY_REQUEST
13. SESSION_SERIALIZER
"""


from django.http import HttpResponse
def post_comment(request):
    if request.session.get('has_commented', False):
        return HttpResponse('Already commented')

    request.session['has_commented'] = True
    return HttpResponse('Commented')


def delete_comment(request):
    try:
        del request.session['has_commented']
    except KeyError:
        pass

    return HttpResponse('Mark deleted')


"""
Использование сессий вне представлений


>>> from django.contrib.sessions.backends.db import SessionStore
>>> s = SessionStore()
>>> s['last_login'] = 1234

Создание новой сессии:
>>> s.create()
>>> s.session_key
'dqeowbxlgbvw5q449mxqyvxb22tpxwe8'
>>> s = SessionStore(session_key='dqeowbxlgbvw5q449mxqyvxb22tpxwe8')
>>> s['last_login']
1234

>>> from django.contrib.sessions.models import Session
>>> s = Session.objects.get(pk='dqeowbxlgbvw5q449mxqyvxb22tpxwe8')
>>> s.expire_date
datetime.datetime(2023, 12, 16, 13, 9, 32, 496473, tzinfo=datetime.timezone.utc)
>>> s.session_data
'eyJsYXN0X2xvZ2luIjoxMjM0fQ:1r9PkS:LyBjyBsNM1FM9__osS9WhXsAyxD5tFBj8LKW2Ii7dS0'
>>> s.get_decoded()
{'last_login': 1234}
"""

"""
Расширение сеансов


base_session.AbstractBaseSession - абстрактная модель базового сеанса.
Методы и атрибуты:
    - session_key - строка, содержащая основной ключ.
    - session_data - строка, содержащая закодированный и сериализованный словарь сеанса.
    - session_expire - дата и время, обозначающие дату окончания сеанса.
    - get_session_store_class() - возвращает класс хранилища сеансов.
    - get_decoded() - возвращает декодированные данные сеанса.


backends.db.SessionStore - реализует хранилище сеансов на базе БД.
Методы и атрибуты:
    - get_model_class() - возвращает модель сеанса.
    - create_model_instance(data) - возвращает новый экземпляр обьекта модели сеанса, который представляет текущее состояние сеанса.


backends.cached_db.SessionStore - реализует кэшированное хранилище сеансов на базе БД.
Методы и атрибуты:
    - cache_key_prefix - префикс, добавляемый к ключу сеанса для создания строки ключа кэша.

    
Пример пользовательского механизма сеансов:
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models


class CustomSession(AbstractBaseSession):
    account_id = models.IntegerField(null=True, db_index=True)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return CustomSession
        
    def create_model_instance(self, data):
        obj = super().create_model_instance(data)
        try:
            account_id = int(data.get('_auth_user_id))
        except (ValueError, TypeError):
            account_id = None
        ojb.account_id = account_id
        return obj


Пример пользовательского механизма сеансов на основе кэша:
class SessionStore(CachedDBStore):
    cache_key_prefix = 'mysessions.custom_cached_db_backed'        
"""



