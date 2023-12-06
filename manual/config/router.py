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