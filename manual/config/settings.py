# Мануал по Django 4.2
# https://docs.djangoproject.com/en/4.2/ref/
# https://docs.djangoproject.com/en/4.2/topics/


from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-_m7#wcewdv(+n%gbx)g5nn*!xhtoqvts5+9jmhr+hc=q!#2hu%'


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # Подключение сессий, поддерживаемых БД
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_manual',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Включения функциональности сессий
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


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