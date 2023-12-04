# Мануал по Django 4.2
# https://docs.djangoproject.com/en/4.2/ref/
# https://docs.djangoproject.com/en/4.2/topics/


import os
from pathlib import Path
import logging


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-_m7#wcewdv(+n%gbx)g5nn*!xhtoqvts5+9jmhr+hc=q!#2hu%'


DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']


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

    'django_manual',
]


# Серверная часть SMTP для отправки электронных писем
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Список механизмов аутентификации
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]
# Модель пользователя
AUTH_USER_MODEL = 'auth.User'
# Список классов алгоритмов хеширования. Django будет использовать PBKDF2
# для хранения паролей, но будет поодерживать проверку паролей, хранящихся с помощью
# PBKDF2SHA1, argon2, bcrypt
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]
# Список валидаторов пароля
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
# Подключение нескольких DB.
Псевдонимы DB могут быть любыми.
migrate работает с default DB:
./manage.py migrate
./manage.py migrate --database=users

Маршрутизаторы DB:
1. db_for_read(model, **hints) - DB для чтения обьектов.
2. db_for_write(model, **hints) - DB для записи обьектов.
3. allow_relation(obj1, obj2, **hints) - разрешена ли связь между obj1 и obj2.
4. allow_migrate(db, app_label, model_name=None, **hints) - разрешено ли выполнение операции миграции в DB с именем db.

DATABASES = {
    "default": {},
    "auth_db": {
        "NAME": "auth_db_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "swordfish",
    },
    "primary": {
        "NAME": "primary_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "spam",
    },
    "replica1": {
        "NAME": "replica1_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "eggs",
    },
    "replica2": {
        "NAME": "replica2_name",
        "ENGINE": "django.db.backends.mysql",
        "USER": "mysql_user",
        "PASSWORD": "bacon",
    },
}

Маршрутизатор для управления запросов в auth приложение:
class AuthRouter:
    route_app_labels = {"auth", "contenttypes"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == "auth_db"
        return None

Маршрутизатор для остальных приложений:
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return random.choice(["replica1", "replica2"])

    def db_for_write(self, model, **hints):
        return "primary"

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {"primary", "replica1", "replica2"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

Добавляем в настройки маршрутизаторы (порядок важен):
DATABASE_ROUTERS = ["path.to.AuthRouter", "path.to.PrimaryReplicaRouter"]
"""


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Обработчики загрузки файлов по умолчанию: чтение небольших файлов в память и больших на диск.
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler'
]


"""
Раздел: Logging (Ведение журнала)


Логирование состоит из 4х частей:
- Loggers (Регистраторы) - точка входа в систему логирования. Может иметь несколько обработчиков.
- Handlers (Обработчики) - определяют что делать с каждым сообщением в журнале. Он описывает конкретное поведение, например, запись в консоль или файл.
- Filters (Фильтры) - обеспечивают доп. контроль между регистратором и обработчиком.
- Formatters (Форматеры) - описывают точный формат вывода сообщения.

Регистратор настроен на уровни логирования:
- DEBUG - Информация, описывающая цели отладки.
- INFO - Информация, описывающая состояние системы.
- WARNING - Информация, описывающая незначительную проблему.
- ERROR - Информация, описывающая серьезную проблему.
- CRITICAL - Информация, описывающая критическую проблему.


Логирование по умолчанию:
django.server регистратор отправляет сообщения в консоль от уровня INFO и выше. 
DEBUG=True:
- django регистратор отправляет сообщения в консоль от уровня INFO.
DEBUG=False:
- django регистратор отправляет сообщения в AdminEmailHandler от уровня ERROR.

Все регистраторы, кроме django.server передают логирование родителям, вплоть до django регистратора.

LOGGING по умолчанию: django.utils.log.DEFAULT_LOGGING.



propagate - передавать ли сообщения родительским обработчикам.



Регистраторы:
1. django - родительский регистратор для сообщений. Обычно не используется. Используются его регистраторы.
2. django.request - сообщения, связанные с обработкой запросов. 5XX - ERROR, 4XX - WARNING. Доп. контекст: status_code, request.
3. django.server - сообщения, связанные с обработкой запросов, полученных сервером. 5XX - ERROR, 4XX - WARNING, остальное - INFO. Доп. контекст: status_code, request.
4. django.template - сообщения, связанные с отрисовкой шаблонов. Отсутствующие переменные контекста регистрируются как DEBUG сообщения.
5. django.db.backends - сообщения, связанные с БД. Регистрируются как DEBUG сообщения. Доп. контекст: duration, sql, params, alias.
6. django.security.* - сообщения, связанные с безопасностью приложения (SuspiciousOperation и т.д.). Например, когда Host заголовок не соответствует ALLOWED_HOSTS, будет 400 в регистраторе django.security.DisallowedHost.
По умолчанию попадают в django регистратор, который отправляет админам сообщения на почту при DEBUG=False. (django.security.csrf, django.security.DisallowedHost)
7. django.db.backends.schema - сообщения, связанные с миграциями БД. Контекст такой же, как у django.backends.



Обработчики:
1. AdminEmailHandler(
    include_html=False, # Включает ли письмо HTML страницы отладки, которое выводится при DEBUG=True.
    email_backend=None, # Переопределение серверной части эл. почты.
    reporter_class=None # Класс для настройки текста обратной трассировки в письме.
) ->  # Отправляет эл. письмо админам ADMINS.



Фильтры:
1. CallbackFilter(callback) - принимает функцию обратного вызова и вызывает ее для каждого сообщения. Должно вернуть True, иначе сообщение не будет пропущено. 
2. RequireDebugFalse - передает сообщение только если DEBUG=False.
3. RequireDebugTrue - противоположен RequireDebugFalse.
"""

LOGGING = {
    'version': 1,
    # Отключение средств логирования по умолчанию. Не рекомендуется менять
    'disable_existing_loggers': False,
    'filters': {
        # Фильтр, который передает записи когда DEBUG=True
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        # Выводит уровень, сообщение, время, процесс, поток и модуль, которые генерируют лог.
        'verbose': {
            'format': '{levelname} - {asctime} - {module} - {message}',
            'style': '{',
        },
        # Выводит уровень и сообщение.
        'simple': {
            'format': '{levelname} - {asctime} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Обработчик для вывода в консоль
        'console': {
            'formatter': 'simple',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        }
    },
    # Родительский регистратор root
    # 'root': {
    #     'handlers': ['console'],
    # },
    'loggers': {
        'django': {
            # 'handlers': ['file'],
            # 'level': 'INFO',
        },
        # 'django.server': {
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        'django.template': {
            # 'handlers': ['console'],
            # 'level': 'DEBUG',
            # 'propagate': False,
        },
        'django.request': {
            # 'handlers': ['console'],
            # 'level': 'INFO',
            # 'propagate': False,
        },
        'django.db.backends': {
            # 'handlers': ['console'],
            # 'level': 'DEBUG',
        },
        'django.db.backends.schema': {
            # 'handlers': ['console'],
            # 'level': 'DEBUG',
        },
        'custom_logger': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}