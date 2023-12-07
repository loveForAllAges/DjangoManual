# 10. Django's cache framework (Фреймворк кеширования Django).


"""
Кешировать значит сохранить результат вычисления, чтобы не пришлось выполнять 
его в следующий раз.

        
Django предлагает различные уровни детализации кэша:
    - кэшировать выходные данные определенных представлений;
    - кэшировать только те части, которые сложно создавать;
    - кэшировать весь сайт.

Django работает с нисходящими кэшами (Squid, браузерный кэш). Это тип 
кэшей, которыми не управляют напрямую, но которым подсказывают (через 
HTTP-заголовки) о том, какие части сайта следует кэшировать и как.




Доступные значения для CACHES.

1. Memcached
    Наиболее частоиспользуемый сервер производственного кэша, основанный на 
    памяти. Работает как демон и ему выделяется опреденный обьем оперативной 
    памяти. Недостаток: так как данные хранятся в памяти, то они будут потеряны 
    в случае сбоя сервера. Макс. длина ключючей кэша 250 символов.
2. Redis
    База данных в памяти. Необходим сервер Redis, работающий локально или на 
    удаленном компе.
3. Database caching
    Хранение кэшированных данных в БД. Лучше всего это работает, если есть 
    быстрый и хорошо индексируемый сервер БД. В отличие от остальных механизмов 
    кэширования, кэш БД не поддерживает автоматический отбор записей с истекшим 
    сроком действия на уровне БД. Вместо этого записи кэша с истекшим сроком 
    действия отбираются каждый раз при вызове add(), set(), touch().
4. Filesystem caching
    Серверная часть на основе файлов сериализует и сохраняет каждое значение 
    кэша в отдельном файле. Злоумышленник, получивший доступ к файлу кэша может 
    не только фальсифицировать HTML-контент, но и удаленно выполнить 
    произвольный код, так как данные сериализуются с помощью pickle. Также 
    кэширование файловой системы может замедляться при хранении большого кол-ва 
    файлов.
5. Local-memory caching
    По умолчанию. Использует стратегию отбраковки наименее недавно 
    испльзованных данных (LRU). Кэш локальной памяти не особенно эффективен с 
    точки зрения использования памяти, поэтому не является хорошим выбором для 
    производственной среды.
6. Dummy caching (Для разработки)
    Фиктивное кэширование. Не кэшируется, а просто реализует интерфейс кэша.
    Это полезно, если есть сайт, который использует интенсивное кэширование в 
    различных местах, но есть среда разработки/тестирования, где вы не хотите 
    кэшировать.
7. Custom cache backend
    Собственная серверная часть кэша.

    
Аргументы кэша.

1. TIMEOUT
2. OPTIONS
2.1. MAX_ENTRIES
2.2. CULL_FREQUENCY
3. KEY_PREFIX
4. VERSION
5. KEY_FUNCTION


Кэширование всего сайта.

Самый простой способ использовать кэширование - кэшировать весь сайт.

Необходимые Middleware:
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
]

Необходимые настройки:
- CACHE_MIDDLEWARE_ALIAS
- CACHE_MIDDLEWARE_SECONDS
- CACHE_MIDDLEWARE_KEY_PREFIX

FetchFromCacheMiddleware кэширует ответы GET и HEAD со статусом 200, если 
позволяют заголовки запроса и ответа. Ответы на запросы одного и того же URL с 
разными параметрами запроса считаются уникальными страницами. Этот middleware 
ожидает, что на запрос HEAD будет получен ответ с теми же заголовками ответа, 
что и на соответствующий запрос GET. В этом случае он может вернуть 
кэшированный ответ GET на запрос HEAD.

UpdateCacheMiddleware устанавливает заголовки в каждом HttpResponse, которые 
влияют на кэш:
    - Устанавливает Expires в текущую дату/время плюс определенный 
    CACHE_MIDDLEWARE_SECONDS.
    - Устанавливает в Cache-Control максимальный возраст страницы из 
    CACHE_MIDDLEWARE_SECONDS.

Если USER_I18N=True, то ключ кэша будет включать имя активного языка, а также 
текущий часовой пояс.


Кэширование страницы.

cache_page(
    timeout, # Тайм-аут в секундах. Приоритет над max-age из Cache-Control.
    *, 
    cache=None, # Кэш из CACHES. По умолчанию default.
    key_prefix=None # то же, что и CACHE_MIDDLEWARE_KEY_PREFIX.
) -> # Автоматически устанавливаются Cache-Control, Expires заголовки в ответе.

Пример:
    from django.views.decorators.cache import cache_page
    path('cached_page/', cached_page),

    @cache_page(60 * 15)
    def cached_page(request, *args, **kwargs):
        a = Author.objects.all()
        return HttpResponse(a)
ИЛИ:
    path('cached_page/', cache_page(60 * 15)(cached_page)),


Кэширование частей шаблона.

Пример:
    {% load cache %}
    {% cache 500 sidebar %}
    ... sidebar ...
    {% endcache %}
ИЛИ с доп. аргументами:
    {% load cache %}
    {% cache 500 sidebar request.user.username %}
    ... sidebar for logged in user ...
    {% endcache %}
ИЛИ если USE_I18N=True:
    {% load i18n %}
    {% load cache %}
    {% get_current_language as LANGUAGE_CODE %}
    {% cache 600 welcome LANGUAGE_CODE %}
        {% translate "Welcome to example.com" %}
    {% endcache %}
ИЛИ с выбором механизма кэширования:
    {% cache 300 using='localcache' %}

    
django.core.cache.utils.make_template_fragment_key(
    fragment_name, # Равен cache.
    vary_on=None # Список доп. аргументов, переданных тегу.
) -> # Получение ключа кэша, используемого для кэшированного фрагмента.


API низкого уровня.

Иногда кэширование всей страницы не дает пользы. Например, на странице есть 
данные, которые меняются с разной периодичностью. Для этого есть API низкого 
уровня. Можно кэшировать любой уровень детализации. Версии кэшей нужны для 
частичной очистки кэша.

cache.set(
    key, # Строка.
    value, # Любой обьект Python.
    timeout=DEFAULT_TIMEOUT, # Время хранения. По умолчанию timeout из CACHES.
    version=None #
)

cache.get(
    key, # 
    default=None, # Возвращаемое значение, если обьект не существует в кэше.
    version=None #
)

cache.add(
    key, # 
    value, # 
    timeout=DEFAULT_TIMEOUT, # 
    version=None, #
) -> # Добавить ключ, если он еще не существует.

cache.get_or_set(
    key, # 
    default, # 
    timeout=DEFAULT_TIMEOUT, # 
    version=None, # 
) -> # Получить или установить значение ключа.

cache.get_many(
    keys, # 
    version=None, # 
) -> # Обращается к кэшу один раз. Возвращает словарь с запрошенными ключами.

cache.set_many(
    dict, # Словарь обьектов.
    timeout, # 
) -> # Эффективное добавление значений. 

cache.delete(
    key, # 
    version=None, # 
) -> # Очистить кэш обьекта. Возвращает True или False.

cache.delete_many(
    keys, # Список ключей
    version=None, # 
) -> # Очистить кэш нескольких обьектов.

cache.clear(
) -> # Удалить все ключи в кэше.

cache.touch(
    key, # 
    timeout=DEFAULT_TIMEOUT, # 
    version=None, # 
) -> # Устанавливает новый срок действия ключа.

cache.incr(
    key, # 
    delta=1, # 
    version=None, # 
) -> # Увеличение существующего ключа.

cache.decr(
    key, # 
    delta=1, # 
    version=None, # 
) -> # Уменьшение существующего ключа.

cache.close(
) -> # Закрыть соеднение с кэшем.

Пример:
    # Доступ к кэшам в CACHES.
    >>> from django.core.cache import caches
    >>> cache1 = caches['default']
    >>> cache2 = caches['default']
    >>> cache1 is cache2
    True
    # Получение кэша по умолчанию.
    >>> from django.core.cache import cache

    # Основное использование
    >>> cache.set('my_key', 'hello, world', 30)
    >>> cache.get('my_key')
    'hello, world'
    # Через 30 секунд кэш будет недоступен



Нисходящее кэширование.

Использование Vary заголовков.
Vary определяет какие заголовки запросов сервер кэширования должен учитывать 
при построении своего ключа кэша. По умолчанию система кэширования создает 
ключи кэша по URL. Чтобы учитывались заголовки (например, файлы cookie, язык, 
пользовательский агент), необходимо использовать Vary заголовок.

from django.views.decorators.vary import vary_on_headers

@vary_on_headers('User-Agent')
def my_view(request):
    pass
    
В этом случае механизм кэширования будет кэшировать страницу для каждого 
уникального User-Agent.

from django.utils.cache import patch_vary_headers

def view(request):
    response = render(request, 'template_name')
    patch_vary_headers(response, ['Cookie'])
    return response

patch_vary_headers принимает HttpResponse и кортеж заголовков.


from django.views.decorators.cache import cache_control

cache_control(private=True)
def view(request):
    pass

    
Указываем, что кэш страницы должен быть частным.
Пример: блог в котором есть публичные записи, а есть частные. Публичные записи 
могут кэшироваться общем кэше.


django.views.decorators.cache.never_cache - декоратор отключения кэширования.
"""