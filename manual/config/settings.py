"""
Файл настроек по умолчанию:
from django.conf.global_settings


python manage.py diffsettings - различия между текущим файлом настроек и настройками по умолчанию.

from django.conf import settings - рекомендуемый способ использоваться настроек.
"""


import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


"""
Основные настройки
"""


# Словарь, сопоставляющий строки с функциями, которые принимают обьект модели и возвращают его URL-адрес.
# Это способ вставки и переопределения get_absolute_url().
# Пример: {'blogs.blog': labmda o: '/blogs/%s/' % o.slug,}
ABSOLUTE_URL_OVERRIDES = {}


# Список людей, которые получают уведомления об ошибках кода.
# Пример: [('John', 'john@gmail.com'),]
ADMINS = []


# Список строк хостов/доменов, которые обслуживает Django.
# Например: 'www.example.com', 'example.com', '*' соответствует всему.
# Если DEBUG=True, то по умолчанию ['.localhost', '127.0.0.1', '[::1]'].
# По умолчанию [].
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']


# Если True, то если URL-адрес не нашел соответствие в URLconf и не заканчивается косой чертой, 
# то HTTP-перенаправление на тот же URL-адрес с добавленной косой чертой.
# Перенаправление может привести к потере данных, отправленных POST запросом.
APPEND_SLASH = True


# Словарь, содержащий настройки для всех кешей проекта.
# Это вложенный словарь, который сопоставляет псеводнимы кеша со словарем, содержащим параметры для отдельного кеша.
# BACKEND - серверная часть кеша. По умолчанию ''.
# KEY_FUNCTION - строка, содержащая путь к функции, которая составляет префикс, версию и ключ  в окончательный ключ хеша.
# KEY_PREFIX - Дополнение к ключам кэша. По умолчанию ''.
# LOCATION - местоположение используемого кеша. По умолчанию ''.
# OPTIONS - доп. параметры для передачи в серверную часть кеша. По умолчанию None.
# TIMEOUT - кол-во секунд до того, как запись в кеше считается устаревшей. None - не имеет срока действия, 0 - не кешировать. По умолчанию 300.
# VERSION - номер версии по умолчанию для ключей кеша. По умолчанию 1.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# Псевдоним кэша, который будет использоваться.
CACHE_MIDDLEWARE_ALIAS = 'default'


# Имя сайта или другая строка, уникальная для этого экземпляра Django, чтобы 
# предотвратить конфиликты ключей. Если кэш используется несколькими сайтами, 
# использующими одну и ту же установку Django. Если все равно, то ''.
# Сочетается с KEY_PREFIX.
CACHE_MIDDLEWARE_KEY_PREFIX = ''


# Кол-во секунд, в течение которых должна кэшироваться каждая страница.
CACHE_MIDDLEWARE_SECONDS = 600


# Возраст файлов cookie CSRF в секундах.
CSRF_COOKIE_AGE = 31449600


# Домен, который будет использоваться при настройке файла cookie CSRF. Полезно для исключения запросов между поддоменами 
# из обычной защиты от подделки межсайтовых запросов.
CSRF_COOKIE_DOMAIN = None


# Использовать ли флаг HttpOnly в файле cookie CSRF. Если True, то клиентский JS не сможет получить доступ к файлу cookie CSRF.
CSRF_COOKIE_HTTPONLY = False


# Имя файла cookie, который будет использоваться в качестве токена аутентификации CSRF.
CSRF_COOKIE_NAME = 'csrftoken'


# Путь, заданный в файле cookie CSRF.
CSRF_COOKIE_PATH = '/'


# Значение флага SameSite в файле cookie CSRF. Этот флаг предотвращает отправку файлов cookie в межсайтовых запросах.
CSRF_COOKIE_SAMESITE = 'Lax'


# Использовать ли безопасный файл cookie для файла cookie CSRF. Если True, то файл cookie отправляется только через HTTPS-соединение.
CSRF_COOKIE_SECURE = False


# Следует ли хранить токен CSRF в сеансе пользователя, а не в файле cookie. Требует django.contrib.sessions.
# Хранение токена в cookie безопасно, но в других фреймворках сохраняется в сеансе. Требует особого порядка списка MIDDLEWARE.
CSRF_USE_SESSIONS = False


# Путь к функции просмотра при отклонении запроса защитой CSRF.
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'


# Имя заголовка запроса, используемого для аутентификации CSRF.
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'


# Список доверенных источников небезопасных запросов.
CSRF_TRUSTED_ORIGINS = []


# Словарь, содержащий настройки для всех БД проекта. Содержит псевдонимы БД со словарями параметров.
# Обязательна настройка default.
# ATOMIC_REQUESTS - оборачивать ли каждое представление в транзакцию в этой БД. По умолчанию False.
# AUTOCOMMIT - Отключать ли управление тразакциями и реализовать собственное. По умолчанию True.
# ENGINE - Используемая БД. По умолчанию ''.
# HOST - Хост БД. По умолчанию '' (локальный хост).
# NAME - Имя БД. По умолчанию ''.
# CONN_MAX_AGE - Время существования соединения с БД в секундах. По умолчанию 0.
# CONN_HEALTH_CHECKS - проверять ли работоспособность постоянного подключения к БД. По умолчанию False.
# OPTIONS - доп. параметры при подключении к БД. По умолчанию {}.
# PASSWORD - пароль БД. По умолчанию ''.
# PORT - порт БД. По умолчанию ''.
# TIME_ZONE - часовой пояс подключения к БД. По умолчанию None.
# DISABLE_SERVER_SIDE_CURSORS - отключить ли использование курсоров на стороне сервера. По умолчанию False.
# USER - имя пользователя БД. По умолчанию ''.
# TEST - Словарь настроек тестовых баз. По умолчанию {}.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Макс. размер тела запроса до SuspiciousOperation. None - отключить проверку. Приложениям, 
# которые получают сообщения большого размера, следует настроить это параметр. 
# Большие запросы могут использоваться в качестве DoS атаки (TODO), если их не контролировать.
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440 # 2,5 MB


# Макс. кол-во параметров GET, POST запросов. None - отключить проверку. 
# Потенциальная угроза та же, что и настройка выше.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# Макс. кол-во файлов POST запроса. None - отключить проверку.
DATA_UPLOAD_MAX_NUMBER_FILES = 100


# Список маршрутизаторов, которые будут использоваться для определения БД при выполнении запроса.
DATABASE_ROUTERS = []


# Форматирование полей даты по умолчанию.
DATE_FORMAT = 'N j, Y' # Feb. 4, 2003


# Список допустимых форматов даты при вводе.
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y",  # '10/25/06'
    "%b %d %Y",  # 'Oct 25 2006'
    "%b %d, %Y",  # 'Oct 25, 2006'
    "%d %b %Y",  # '25 Oct 2006'
    "%d %b, %Y",  # '25 Oct, 2006'
    "%B %d %Y",  # 'October 25 2006'
    "%B %d, %Y",  # 'October 25, 2006'
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 October, 2006'
]


# Форматирование полей даты и времени по умолчанию.
DATETIME_FORMAT = 'N j, Y, P' # Feb. 4, 2003, 4 p.m.


# Список допустимых форматов даты и времени при вводе.
DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]


# Логическое значение, которое включает/выключает режим отладки.
# При True запоминается каждый SQL-запрос. Если False, то необходимо настроить ALLOWED_HOSTS.
# По умолчанию False.
DEBUG = True


# Пропускать ли handler500 и представления отладки.
DEBUG_PROPAGATE_EXCEPTIONS = False


# Разделитель десятичных чисел.
DECIMAL_SEPARATOR = '.'


# Тип поля первичного ключа для моделей у которых не поля с атрибутом primary_key=True.
# По умолчанию 'django.db.models.AutoField'.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Кодировка по умолчанию для HttpResponse, если MIME не указан. 
# Используется при генерации Content-Type заголовка.
DEFAULT_CHARSET = 'utf-8'


# Генератор отчета об исключениях.
DEFAULT_EXCEPTION_REPORTER = 'django.views.debug.ExceptionReporter'


# Фильтр информации об исключениях при отчете об ошибках.
DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'


# эпочта для отправки писем. Не входят сообщения об ошибках отправленные ADMINS, MANAGERS, для этого SERVER_EMAIL.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'


# Табличное пространство для индексов по полям.
DEFAULT_INDEX_TABLESPACE = ''


# Табличное пространство для моделей в которых оно не указано.
DEFAULT_TABLESPACE = ''


# Список скомпилированных обьектов рег. выражений, представляющих строки User-Agent, 
# которым не разрешено посещать сайт. Защита от ботов/сканеров. Используется если CommonMiddleware установлено.
DISALLOWED_USER_AGENTS = []


# Серверная часть SMTP для отправки электронных писем
EMAIL_BACKEND = 'django.core.mail.backends.smpt.EmailBackend'


# Каталог для хранения выходных файлов.
EMAIL_FILE_PATH = None


# Хост для отправки эпочты.
EMAIL_HOST = 'localhost'


# Пароль для SMTP-сервера.
EMAIL_HOST_PASSWORD = ''


# Имя пользователя для SMTP-сервера.
EMAIL_HOST_USER = ''


# Порт для SMTP-сервера.
EMAIL_PORT = 25


# Префикс темы для сообщений эпочты в mail_admins() и mail_managers().
EMAIL_SUBJECT_PREFIX = '[Django] '


# Отправлять заголовок Date сообщений SMTP эпочты в местном часовом поясе (True) или в формате UTC (False).
EMAIL_USE_LOCALTIME = False


# Использовать ли TLS соединение при общении с SMTP-сервером.
EMAIL_USE_TLS = False


# Использовать ли неявное соединение TLS при общении с SMTP-сервером. Или это или EMAIL_USE_TLS.
EMAIL_USE_SSL = False


# Доп. путь к файлу цепочки сертификатов в формате PEM для SSL-соединения.
EMAIL_SSL_CERTFILE = None

# Доп. путь к файлу закрытого ключа в формате PEM для SSL-соединения.
EMAIL_SSL_KEYFILE = None


# Указывает тайм-аут в секундах для блокировки операций, таких как попытка подключения.
EMAIL_TIMEOUT = None


# Список обработчиков загрузки файлов по умолчанию: чтение небольших файлов в память и больших на диск.
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]


# Макс. размер в байтах, который будет иметь загрузка, прежде чем будет передана в файловую систему.
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 # 2,5 MB


# Числовой режим, применяемый к каталогам, созданным в процессе загрузки файлов.
# Также определяет разрешения по умолчанию для собранных статических каталогов.
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None


# Числовой режим для установки вновь загружаемых файлов. Подробнее os.chmod().
FILE_UPLOAD_PERMISSIONS = 0o644


# Каталог для временного хранения данных размером больше FILE_UPLOAD_MAX_MEMORY_SIZE 
# во время загрузки файлов.
FILE_UPLOAD_TEMP_DIR = None


# Число, обозначающее первый день недели. Используется при отображении календаря.
FIRST_DAY_OF_WEEK = 0 # Воскресенье


# Список каталогов, в которых осуществляется поиск fixture файлов.
FIXTURE_DIRS = []


# Значение переменной SCRIPT_NAME в HTTP-запросе.
FORCE_SCRIPT_NAME = None


# Класс, который отображает формы и виджеты форм. Реализует низкоуровневый API рендеринга.
FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'


# Использовать ли https в качестве нового значения по умолчанию URLField.assume_scheme.
FORMS_URLFIELD_ASSUME_HTTPS = False


# Полный путь к пакету, который содержит определение формата локалей проекта.
FORMAT_MODULE_PATH = None


# Список скомпилированных обьектов регулярных выражений, описывающих URL-адреса, 
# которые следует игнорировать при сообщении об ошибках HTTP 404 по эпочте.
# Например, favicon.ico.
IGNORABLE_404_URLS = []


# Список строк путей к классу конфигурации приложения или пакета с приложением.
# По умолчанию [].
INSTALLED_APPS = [
    'django.contrib.admin',
    # Ядро структуры аутентификации и ее модели по умолчанию. Создание разрешений по умолчанию (CRUD) для каждой модели.
    'django.contrib.auth',
    # Система типов контента, которая позволяет связывать разрешения с моделями
    'django.contrib.contenttypes',
    # Подключение сессий, поддерживаемых БД
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'dja',
    'drf',
]


# Список IP-адресов для получения более подробных отладки приложения.
INTERNAL_IPS = []


# Строка с кодом языка из LANGUAGES для перевода сайта. Необходим USE_I18N.
LANGUAGE_CODE = 'en-us'


# Возраст языкового файла cookie в секундах.
LANGUAGE_COOKIE_AGE = None # Истекает при закрытии браузера.


# Домен, который будет использоваться для языкового файла cookie для междоменных файлов cookie.
LANGUAGE_COOKIE_DOMAIN = None

# Использовать ли HttpOnly в языковом файле cookie. Если True, то клиентский JS не сможет получить к файлу.
LANGUAGE_COOKIE_HTTPONLY = False


# Имя файла cookie, который будет использоваться для языкового файла cookie.
LANGUAGE_COOKIE_NAME = 'django_language'


# TODO Что такое языковой файле cookie.
# Создать мультиязычный сервис.


# Путь, заданный в языковом файле cookie. Соответствует либо URL-адресу установки Django, 
# либо быть родительским для этого пути. Это полезно если есть несколько экземпляров Django,
# работающих под одним и тем же именем хоста. Они могут использовать разные пути к файлам cookie, 
# и каждый экземпляр будет видеть только свой собственный языковой файл cookie.
LANGUAGE_COOKIE_PATH = '/'


# Значение флага SameSite в языковом файле cookie.
# Этот файл предотвращает отправку файлов cookie в межсайтовых запросах.
LANGUAGE_COOKIE_SAMESITE = None


# Использовать ли безопасный файл cookie для языкового файла cookie. 
# Если True, то файл cookie отправляется только через HTTPS-соединение.
LANGUAGE_COOKIE_SECURE = False


# Список всех доступных языков
# LANGUAGES = [] # django.conf.global_settings


# Список всех языковых кодов справа налево.
# LANGUAGES_BIDI = [] # django.conf.global_settings


# Список каталогов с файлами переводов.
LOCALE_PATHS = []


# Данные о конфигурации, которые передаются методу конфигурации LOGGIN_CONFIG.
# LOGGING = {} # По умолчанию django.utils.log


# Путь к обьекту, который будет использоваться для настройки ведения логирования в проекте.
LOGGING_CONFIG = 'logging.config.dictConfig'


# Список в формате ADMINS тех, кто должен получать уведомления о неработающих 
# ссылках когда BrokenLinkEmailsMiddleware включен.
MANAGERS = []


# Абсолютный путь в файловой системе к каталогу с загруженными пользователями файлами.
MEDIA_ROOT = ''


# URL-адрес, который обрабатывает файлы MEDIA_ROOT, используемые для управления сохраненными файлами.
# Для использования в шаблонах - {{ MEDIA_URL }}, необходимо добавить 'django.template.context_processors.media' в TEMPLATES.
MEDIA_URL = ''


# Список промежуточного программного обеспечения. По умолчанию None.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Управление сеансами по запросам
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Связывает пользователей с запросами, используя сеансы
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Подключение кастомного middleware
    'config.middleware.SimpleMiddleware',
]


# Словарь, определяющий пакет, в котором можно найти модули миграции для каждого приложения.
# Имя пакета по умолчанию для модулей миграции migrations.
MIGRATION_MODULES = {}


# Форматирование для полей даты, когда отображаются только месяц и день.
MONTH_DAY_FORMAT = 'F j'


# Кол-во цифр, сгруппированных вместе в целой части числа. Обычно используется для отображения разделителя тысяч.
# Если параметр больше 0, то будет использоваться разделитель THOUSAND_SEPARATOR.
NUMBER_GROUPING = 0


# Добавлять ли префикс www. для URL-адресов, у которых его нет. Используется если CommonMiddleware установлено.
PREPEND_WWW = False


# Полный путь корневой конфигурации URL.
ROOT_URLCONF = 'config.urls' # По умолчанию None


# Секретный ключ. Используется для обеспечения криптографической подписи. 
# Используется в сессиях, сообщениях, PasswordResetView, криптографических подписях.
SECRET_KEY = 'django-insecure-_m7#wcewdv(+n%gbx)g5nn*!xhtoqvts5+9jmhr+hc=q!#2hu%' # По умолчанию ''


# Список резервных секретных ключей. Используются для изменения SECRET_KEY.
SECRET_KEY_FALLBACKS = []


# Устанавливать ли SecurityMiddleware заголовок X-Content-Type-Options: nosniff. (TODO)
SECURE_CONTENT_TYPE_NOSNIFF = True


# SecurityMiddleware устанавливает заголовок Cross-Origin Opener Policy. (TODO)
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'


# SecurityMiddleware устанавливает includeSubDomains директиву в заголовок HTTP Strict Transport Security.
# Имеет эффект, если SECURE_HSTS_SECONDS = 0.
SECURE_HSTS_INCLUDE_SUBDOMAINS = False


# SecurityMiddleware добавляет preload директиву в HTTP Stict Transport Security заголовок.
# Не имеет эффекта, если SECURE_HSTS_SECONDS не ноль.
SECURE_HSTS_PRELOAD = False


# Если не нулевое значение, то SecurityMiddleware устанавливает HTTP Strict Transport Security заголовок. 
SECURE_HSTS_SECONDS = 0


# Кортеж комбинаций HTTP-заголовков и значений для определения безопасности запроса. Управляет поведением метода обьекта
# запроса is_secure(). По умолчанию is_secure() проверяет, что URL-адрес использует https://. Это важно для защиты CSRF.
# Пример: ('HTTP_X_FORWARDED_PROTO', 'https'). Рекомендуется менять этот параметр только если: (TODO)
# 1. Приложение находится за прокси; 2. Прокси-сервер удаляет X-Forwarded-Proto заголовок; 3. Прокси устанавливает X-Forwarded-Proto заголовок.
SECURE_PROXY_SSL_HEADER = None


# Если URL-адрес соответствует регулярному выражению в списке, запрос не будет перенаправлен на HTTPS. 
# SecurityMiddleware удаляет начальные / из URL, поэтому шаблоны не должны включать их.
# Например, [r'no-ssl/$']. Если SECURE_SSL_REDIRECT=False, то параметр не имеет эффекта.
SECURE_REDIRECT_EXEMPT = []


# SecurityMiddleware устанавливает Referrer Policy заголовок.
SECURE_REFERRER_POLICY = 'same-origin'


# URL на который проходит перенаправление.
# Если SECURE_SSL_REDIRECT=False, то параметр не имете эффекта.
SECURE_SSL_HOST = None


# Все запросы кроме HTTPS, перенаправляются на HTTPS.
SECURE_SSL_REDIRECT = False


# Словарь модулей, содержащий определения сериализатора с ключом строкового идентификатора для типа сериализации.
# Пример: {'yaml': 'path.to.yaml_serializer'}
SERIALIZATION_MODULES = None


# Эпочта с которой приходят сообщения об ошибках для ADMINS и MANAGERS.
SERVER_EMAIL = 'root@localhost'


# Форматирование полей даты в шаблонах.
SHORT_DATE_FORMAT = 'm/d/Y' # 12/31/2003


# Форматирование полей даты и времени в шаблонах.
SHORT_DATETIME_FORMAT = 'm/d/Y P' # 12/31/2003 4 p.m.


# Серверная часть для подписи файлов cookie и других данных.
SIGNING_BACKEND = 'django.core.signing.TimestampSigner'


# Список идентификаторов сообщений, созданных системой проверки системы, которые будут игнорироваться.
SILENCED_SYSTEM_CHECKS = []


# Словарь, содержащий настройки для всех хранилищ проекта. Это вложенный словарь, 
# содержимое которого сопоставляет псевдоним хранилища со словарем параметров хранилища.
STORAGES = {
    # Для управления файлами.
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # для управления статическими файлами.
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Список настроек для всех механизмов шаблонов проекта. По умолчанию [].
# BACKEND - Серверная часть шаблона. По умолчанию None.
# NAME - Псевдоним для шаблонизатора. По умолчанию имя модуля предпоследняя часть BACKEND.
# DIRS - каталоги исходных файлов шаблонов. По умолчанию [].
# APP_DIRS - должен ли движок исктаь исходные файлы внутри приложений. По умолчанию False.
# OPTIONS - доп. параметры для передачи в серверную чатсь шаблона. По умолчанию {}.
TEMPLATES = [
    {
        # путь к классу шаблонов, реализующий API шаблонов Django.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Список каталогов, в которых движок должен искать исходные файлы шаблонов в порядке поиска.
        'DIRS': [],
        # Должен ли движок искать шаблоны внутри установленных приложений.
        'APP_DIRS': True,
        # Настройки для серверной части.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Имя класса для запуска набора тестов.
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Список приложений для отключения отката после проведения тестирования.
TEST_NON_SERIALIZED_APPS = []


# Разделитель тысяч при форматировании чисел. Используется, если USE_THOUSND_SEPARATOR=TRUE и NUMBER_GROUPING>0.
THOUSAND_SEPARATOR = ','


# Форматирование полей времени.
TIME_FORMAT = 'P' # 4 p.m.


# Список валидных форматов времени.
TIME_INPUT_FORMATS = [
    "%H:%M:%S",  # '14:30:59'
    "%H:%M:%S.%f",  # '14:30:59.000200'
    "%H:%M",  # '14:30'
]


# Строка представляющая часовой пояс. Если USE_TZ=False, то это рабочий часовой пояс, 
# иначе это часовой пояс по умолчанию.
TIME_ZONE = 'UTC' # По умполчанию 'America/Chicago'


# Включение системы перевода. Оключение повышает производительность.
USE_I18N = True


# Следует ли отображать числа с использованием разделителя тысяч.
USE_THOUSAND_SEPARATOR = False


# Будет ли datetime учитывать часовой пояс по умолчанию.
USE_TZ = True


# Следует ли использовать X-Forwarded-Host заголовок вместо Host. Необходимо, если используется прокси-сервер, 
# который устанавливает этот заголовок. Имеет приоритет перед USE_X_FORWARDED_PORT.
USE_X_FORWARDED_HOST = False


# Следует ли использовать X-Forwarded-Port заголовок вместо SERVER_PORT META переменной. Необходимо, 
# если используется прокси-сервер, который устанавливает этот заголовок. 
# Имеет приоритет перед USE_X_FORWARDED_HOST.
USE_XFORWARDED_PORT = False


# Путь к приложению WSGI, который будет использовать серверы Django.
WSGI_APPLICATION = 'config.wsgi.application' # По умолчанию None


# Форматирование полей даты, когда отображается год и месяц.
YEAR_MONTH_FORMAT = 'F Y'


# Значение заголовка X-Frame-Options, используемого XFrameOptionsMiddleware.
X_FRAME_OPTIONS = 'DENY'



"""
Конец основных настроек
"""



"""
Настройки авторизации, аутентификации
django.contrib.auth
"""



# Список серверных классов аутентификации, которые используются при аутентификации пользователя.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]


# Модель пользователя.
AUTH_USER_MODEL = 'auth.User'


# URL или имя URL по которому запросы перенаправляются после входа в систему.
LOGIN_REDIRECT_URL = '/accounts/profile/'


# URL или имя URL по которому перенаправляются запросы для входа в систему.
LOGIN_URL = '/accounts/login/'


# URL или имя URL по которому перенаправляются запросы после выхода из системы.
LOGOUT_REDIRECT_URL = None


# Кол-во секунд в течение которых действительна ссылка сброса пароля. Используется в PasswordResetConfimView.
PASSWORD_RESET_TIMEOUT = 259200 # 3 дня в секундах


# Список классов алгоритмов хеширования. Django будет использовать PBKDF2
# для хранения паролей, но будет поодерживать проверку паролей, хранящихся с помощью
# PBKDF2SHA1, argon2, bcrypt
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Список валидаторов пароля для проверки надежности паролей пользователя. По умолчанию [].
AUTH_PASSWORD_VALIDATORS = [
    # Проверяет сходство парооля и атрибутов пользователя. Принимает user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0,7.
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Проверяет, соответствует ли пароль минимальной длине. Принимает min_length=8.
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    # Проверяет, встречается ли пароль в списке общих паролей. Принимает password_list_path=DEFAULT_PASSWORD_LIST_PATH.
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # Проверяет, является ли пароль числовым.
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



"""
Конец настроек авторизации, аутентификации
"""



"""
Настройки сообщений
django.contrib.messages
"""



from django.contrib import messages
# Минимальный уровень записываемых сообщений
MESSAGE_LEVEL = messages.INFO


# Место хранения сообщений.
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'


# Сопоставление уровня сообщения с тегом сообщения для HTML. При обновлении указать только новые значения.
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}



"""
Конец настроек сообщений
"""



"""
Настройки сессий
django.contrib.sessions
"""


# Место используемого кеша при использовании хранилища сеансов на основе кеша.
SESSION_CACHE_ALIAS = 'default'


# Возвраст файлов cookie сеанса.
SESSION_COOKIE_AGE = 1209600 # 2 недели в секундах


# Домен для файлов cookie сеанса.
SESSION_COOKIE_DOMAIN = None


# Следует ли использовать HttpOnly флаг в файле cookie сеанса. Если True, то клиентский JS не сможет получить доступ к файлу.
SESSION_COOKIE_HTTPONLY = True


# Имя файла cookie сеанса.
SESSION_COOKIE_NAME = 'sessionid'


# Путь, заданный в файле cookie сеанса.
SESSION_COOKIE_PATH = '/'


# Значение флага SameSite в файле cookie сеанса. Предотвращает отправку cookie в межсайтовых запросах, 
# что предотвращает атаки CSRF и делает невозможными некоторые кражи файлов cookie сеанса.
SESSION_COOKIE_SAMESITE = 'Lax'


# Следует ли использовать безопасный файл cookie сеанса. Гарантирует отправку через HTTPS.
SESSION_COOKIE_SECURE = False


# Место хранения данных сеанса.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


# Следует ли завершать сеанс, когда пользователь закрывает браузер.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Каталог хранения данных сеанса при использовании файлового хранилища сеансов.
SESSION_FILE_PATH = None


# Следует ли сохранять данные сеанса при каждом запросе.
SESSION_SAVE_EVERY_REQUEST = False


# Полный путь сериализатора для данных сеанса.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'



"""
Конец настроек сессий
"""



"""
Настройки сайтов
django.contrib.sites
"""



# ID текущего сайта в django_site БД. Используется для того, чтобы данные приложеня могли 
# подключаться к определнным сайтам, а одна БД могла управлять содержимым нескольких сайтов.
SITE_ID = None



"""
Конец настроек сайтов
"""



"""
Настройки статических файлов
django.contrib.staticfiles
"""



# Путь к каталогу в котором будут собираться статические файлы.
STATIC_ROOT = None


# URL статических файлов, расположенных в формате STATIC_ROOT.
STATIC_URL = 'static/' # По умолчанию None


# Список строк, которые содержат полные пути к каталогам доп. файлов.
STATICFILES_DIRS = []


# Список серверов поиска, которые умеют находить статические файлы в разных местах.
# По умолчанию будут найдены файлы в STATICFILES_DIRS и в static каждого приложения.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


"""
Конец настроек статических файлов
"""

"""
Настройки DRF
rest_framework
"""


"""
rest_framework.settings.api_settings

Основные настройки:
REST_FRAMEWORK = {
    # # # Настройки политики API


    # Список или кортеж классов рендереров, определяющий набор рендереров по умолчанию, которые
    # могут быть использованы при возврате обьекта Response.
    # По умолчанию:
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],

    # Список или кортеж классов парсеров, определяющий набор парсеров по умолчанию, 
    # используемых при обращении к свойству request.data
    # По умолчанию:
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser
    ],

    # Список или кортеж классов аутентификации, определяющий набор аутентификаторов по умолчанию, 
    # используемых при обращении к свойствам request.user или request.auth
    # По умолчанию:
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],

    # Список или кортеэ классов разрешений, который определяет набор разрешений по умолчанию,
    # проверяемых при запуске представления. Разрешение должно быть предоставлено каждым классом в списке
    # По умолчанию:
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],

    # Список или кортеж классов дросселей, который определяет набор дросселей по умолчанию, 
    # проверяемых при запуске представления
    # По умолчанию:
    'DEFAULT_THROTTLE_CLASSES': [],

    # Класс согласования содержимого, который определяет, как выбирается рендерер для ответа,
    # учитывая входящий запрос
    # По умолчанию:
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': [
        'rest_framework.negotiation.DefaultContentNegotiation'
    ],

    # Класс инспектора представлений, который будет использоватся для генерации схемы
    # По умолчанию:
    'DEFAULT_SCHEMA_CLASS': [
        'rest_framework.schemas.openai.AutoSchema'
    ],



    # # # Общие настройки представления

    

    # Список классов бэкенда фильтра, которые должны использоваться для общей фильтрации.
    # Если установлено значение None, то общая фильтрация отключена.
    # По умолчанию:
    'DEFAULT_FILTER_BACKENDS': [],

    # Класс по умолчанию, используемый для пагинации наборов зарпосов.
    # Если установлено значение None, пагинация по умолчанию отключена.
    # По умолчанию:
    'DEFAULT_PAGINATION_CLASS': None,

    # Размер страницы по умолчанию, используемый для пагинации.
    # Если установлено значение None, то по умолчанию пагинация отключена.
    # По умолчанию:
    'PAGE_SIZE': None,

    # Имя параметра запроса, который может быть использован для указания поискового термина,
    # используемого SearchFilter
    # По умолчанию:
    'SEARCH_PARAM': 'search',

    # Имя параметра запроса, который может быть использован для указания упорядочения результатов,
    # возвращаемых OrderingFilter
    # По умолчанию:
    'ORDERING_PARAM': 'ordering',

    

    # # # Настройки версий

    

    # Значение, которое должно использоваться для request.version,
    # когда информация о версиях отсутствует.
    # По умолчанию:
    'DEFAULT_VERSION': None,

    # Если задано, это значение ограничивает набор версий, которые могут быть возвращены схемой версий
    # и вызывает ошибку, если предоставленная версия не входит в этот набор.
    # По умолчанию:
    'ALLOWED_VERSIONS': None,

    # Строка, которая должна использоваться для любых параметров версионирования,
    # например, в типе медиа или параметрах запроса URL.
    # По умолчанию:
    'VERSION_PARAM': 'version',

    # Схема версионирования, используемая по умолчанию.
    # По умолчанию:
    'DEFAULT_VERSIONING_CLASS': None,

    

    # # # Настройки аутентификации

    

    # Класс, который должен использоваться для инициализации request.user для неаутентифицированных запросов.
    # Если аутентификация полностью удалена, например, путем удаления django.contrib.auth из INSTALLED_APPS, установите значение None.
    # По умолчанию:
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',

    # Класс, который должен использоваться для инициализации request.auth для неаутентифицированных запросов
    # По умолчанию:
    'UNAUTHENTICATED_TOKEN': None,


    
    # # # Настройки тестов
        

    
    # Формат по умолчанию, который следует использовать при составлении тестовых запросов.
    # Он должен совпадать с форматом одного из классов рендереров в настройке TEST_REQUEST_RENDERER_CLASSES.
    # По умолчанию:
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',

    # Классы рендереров, которые поддерживаются при построении тестовых запросов.
    # Формат любого из этих классов рендереров может быть использован при построении тестового запроса, например: client.post('/users', {'username': 'jamie'}, format='json').
    # По умолчанию:
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],

    

    # # # Элементы управления генерацией схемы

    

    # Если задано, то при генерации параметра пути к схеме идентификатор 'pk' в URL conf сопоставляется с реальным именем поля.
    # Обычно это 'id'. Это дает более подходящее представление, поскольку первичный ключ - деталь реализации, тогда как идентификатор - более общая концепция.
    # По умолчанию:
    'SCHEMA_COERCE_PATH_PK': True,

    # Если установлено, это используется для сопоставления внутренних имен методов набора представлений именами внешних действий, используемых при генерации схемы.
    # Это позволяет нам генерировать имена, более подходящие для внешнего представления, чем те, которые используются внутри кодовой базы.
    # По умолчанию:
    'SCHEMA_COERCE_METHOD_NAMES': {'retrieve': 'read', 'destroy': 'delete'},

    

    # # # Контроль типа содержимого

    

    # Имя параметра URL, который можно использовать для переопределния стандартного повдеения заголовка согласования содержимого Accept,
    # используя параметр запроса format=... в URL запроса.
    # По умолчанию:
    'URL_FORMAT_OVERRIDE': 'format',

    # Имя параметра в URL conf, который может быть использован для обеспечения суффикса формата. 
    # Этот параметр применяется при использовании format_suffix_patterns для включения суффиксных шаблонов URL.
    # По умолчанию:
    'FORMAT_SUFFIX_KWARG': 'format',

    

    # # # Форматирование даты и времени

    

    # Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора
    # DateTimeField. Если None, то поля сериализатора DateTimeField будут возвращать обьекты Python datetime, а кодировка времени будет определяться рендерером.
    # Может быть любым ил None, iso-8601 или строкой Python strftime format.
    # По умолчанию:
    'DATETIME_FORMAT': 'iso-8601',

    # Список форматных строк, которые должны использоваться по умолчанию при разборе входных данных 
    # для полей сериализатора DateTimeField.
    # Может быть списком, включающим строку 'iso-8601' или строки Python strfime format.
    # По умолчанию:
    'DATETIME_INPUT_FORMATS': ['iso-8601],

    # Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора DateField. Если None, то поля сериализатора DateField будут
    # возвращать обьекты Python date, а кодировка даты будте определяться рендерером. 
    # Может быть любым ил None, iso-8601 или строкой Python strftime format.
    # По умолчанию:
    'DATE_FORMAT': 'iso-8601',

    # Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора TimeField. Если None, то поля сериализатора TimeField будут
    # возвращать обьекты Python time, а кодировка времени будет определяться рендерером.
    # Может быть любым ил None, iso-8601 или строкой Python strftime format.
    # По умолчанию:
    'TIME_FORMAT': 'iso-8601',

    # Список форматных строк, которые должны использоваться по умолчанию при разборе входных данных для полей сериализатора TimeField.
    # Может быть списком, включающим строку 'iso-8601' или строки Python strfime format.
    # По умолчанию:
    'TIME_INPUT_FORMATS': ['iso-8601'],



    # # # Кодировки



    # Если установлено, ответы JSON будут разрешать использование символов юникода в ответах. Наример: {'unicode black star': '*'}, иначе {"unicode black star":"\u2605"}.
    # Оба стиля соответствуют RFC 4627. Стиль unicode предпочтительнее, так как более удобен при проверке.
    # По умолчанию:
    'UNICODE_JSON': True,

    # Если установлено значение, ответы JSON будут возвращать компактные представления, без пробелов после символов : и ,.
    # Например: {"is_admin":false,"email":"jane@example"}, иначе {"is_admin": false, "email": "jane@example"}.
    # По умолчанию возвращаются минифицированные ответы.
    # По умолчанию:
    'COMPACT_JSON': True,

    # Если установлено, при рендеринге и разборе JSON будет использоваться только синтаксически правильный JSON, создавая исключение для расширенных значений float (nan, inf),
    # принимаемых модулем Python json. Это рекомендуемая настройка, так как эти значения обычно не поддерживаются. Если False, рендеринг и парсинг JSON будут разрешительными.
    # Однако эти значения все еще не действительны и должны быть специально обработаны в коде.
    # По умолчанию:
    'STRICT_JSON': True,

    # При возврате десятичных обьектов в представлениях API, которые не поддерживают собственный десятичный тип,
    # обычно лучше всего возвращать значение в виде строки. Это позволяет избежать потери точности. Если True, сериализатор класса DecimalField будет возвращать строку, а не Decimal. Иначе будет возвращать Decimal, а кодировщик JSON будет возвращать float.
    # По умолчанию:
    'COERCE_DECIMAL_TO_STRING': True,



    # # # Названия и описания представлений



    # Строка, представляющая функцию, которая должна использоваться при генерации имен представлений.
    # Это должна быть функция со следующей сигнатурой: view_name(self).
    # По умолчанию:
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',

    # Строка, представляющая функцию, которая должна использоваться при генерации описаний представлений.
    # Это должна быть функция со следующей сигнатурой: view_description(self, html=False).
    # По умолчанию:
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',

    # Глобальная настройка значения html_cutoff. Должно быть целое число.
    # В просматриваемом API.
    # По умолчанию:
    'HTML_SELECT_CUTOFF': 1000,

    # Глобальная настройка значения html_cutoff_text.
    # В просматриваемом API.
    # По умолчанию:
    'HTML_SELECT_CUTOFF_TEXT': 'More than {count} items...',



    # # # Разные настройки



    # Строка, представляющая функцию, которая должна быть использована при возврате ответа для любого данного исключения.
    # Если функция возвращает None, то будет ошибка 500. Это должна быть функция со следующей сигнатурой: exception_handler(exc, context).
    # По умолчанию:
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',

    # Строка, представляющая ключ, который следует использовать для ошибок сериализатора, 
    # которые не относятся к конкретному полю.
    # По умолчанию:
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # Строка, представляющая ключ, который должен использоваться для полей URL, генерируемых HyperlinkedModelSerializer. 
    # По умолчанию:
    'URL_FIELD_NAME': 'url',

    # Целое число, равное 0 или более, которое может использоваться для указания количества прокси-серверов приложений, за которыми работает API.
    # Это позволяет дросселированию более точно определять IP-адреса клиентов. Если установлено значение None, то классы дросслеирования будут использовать менее строгое сопоставление IP-адресов.
    # По умолчанию:
    'NUM_PROXIES': None,
}
"""


"""
Конец настроек DRF
"""