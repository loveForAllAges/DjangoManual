from django.contrib import admin
from django.urls import path, include
from .sessions import post_comment, delete_comment


"""
Как Django обрабатывает запрос


1. Определяется корневой модуль URLconf это значение ROOT_URLCONF или urlconf из входящего HttpRequest если есть.
2. Загружается этот модуль и ищет переменную urlpatters (список django.urls.path или django.urls.re_path).
3. По порядку ищет первый совпадающий шаблон URL-адреса, соответствующий path_info.
4. При совпадении импортируется и вызывается данное представление (функция Python) и передаются аргументы: HttpRequest; аргументы ключевого слова **kwargs.
5. Если совпадений нет, возникает соответствующее исключение.
"""

"""
Functions for use in URLconfs - Функции для использования в URLconfs


django.urls:
1. path(route: str, view, kwargs=None, name=None)
Возвращает элемент для включения в urlpatterns. 
route должен быть строкой или gettext_lazy(), может содержать угловые скобки (<int:section>).

2. repath(route: str, view, kwargs=None, name=None)
Возвращает элемент для включения в urlpatterns. 
route должен быть строкой или gettext_lazy(), может содержать регулярное выражение (r"^bio/(?P<username>\w+)/$").

3. include(module, namespace=None)
3. include(pattern_list)
3. include((pattern_list, app_namespace), namespace=None)
Функция, которая передает полный путь импорта модуля. 
Принимает либо итерацию, возвращающую шаблоны URL-адресов, либо кортеж из друх элементов, содержащий эту итерацию + имена пространств имен приложения (module: имя модуля URLconf; namespace: пространство имен экземпляра для вкл. записей URL-адресов; pattern_list: итерируемый path() или repath() экземпляры; app_namespace: пространство имен приложения).

4. register_converter(converter, type_name)
Функция регистрации конвертера для использования в path() (converter: класс преобразователя; type_name: имя преобразователя).

django.conf.urls:

1. static(prefix, view=django.views.static.serve, **kwargs)
Вспомогательная фукнция для возврата шаблона URL-адреса для обслуживания файлов в режиме отладки. static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

2. handler400
Представление. которое следует вызывать, если HTTP-клиент отправил запрос, вызвавший ошибку 400. По умолчанию django.views.defaults.bad_request(). Принмает request, exception. Должно возвращать HttpResponseBadRequest.

3. handler403
Представление, которое следует вызывать, если у пользователя нет разрешений доступа. По умолчанию django.views.defaults.permission_denied(). Принимает request, exception. Должно возвращать HttpResponseForbidden.

4. handler404
Представление, которое следует вызвать, если ни один из шаблонов URL-адресов не соответствует. По умолчанию django.views.defaults.page_not_found(). Принимает request, ecxeption. Должно возвращать HttpResponseNotFound.

5. handler500
Представление, которое следует вызвать в случае ошибок сервера. По умолчанию django.views.defaults.server_error(). Принимает request. Должно возвращать HttpResponseServerError.

Пример:
handler404 = "mysite.views.my_custom_page_not_found_view"
"""

"""
Преобразователи путей


1. str - любая непустая строка, кроме /.
2. int - 0 или любое положительное целое число.
3. slug - любая короткая строка из букв или цифр ASCII, дефиса и подчеркиваний.
4. uuid - отформатированный uuid. 
5. path - любая непустая строка, включая /.
"""

"""
Использование


path("articles/2003/", views.special_case_2003),

Также можно передавать дополнительные опции
path("articles/2003/", views.special_case_2003, {'data': 'text'}),

re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),


Способы получения полного пути представления:
1. url тег в шаблоне.
2. reverse() - в python коде.
3. get_absolute_url() - в модели Django.


Вложенные пространства имен:
name='sports:polls:index'
"""


urlpatterns = [
    path('api/', include('drf.urls')),
    path('', include('dja.urls')),
    path('admin/', admin.site.urls),
    path('test_session', post_comment),
    path('delete_session', delete_comment),
]
