import unicodedata
import warnings

from django.contrib import auth
from django.apps import apps
from django.utils.deprecation import RemovedInDjango51Warning
from django.db import models
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.crypto import salted_hmac, get_random_string
from django.contrib.auth import password_validation
from django.utils.itercompat import is_iterable

from django.contrib.auth.models import (
    _user_get_permissions, _user_has_perm, Group, Permission,
    _user_has_module_perms
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Exists, Q
from django.utils.inspect import func_supports_parameter
from django.utils.deprecation import RemovedInDjango50Warning


"""
Валидаторы
django.contrib.auth.password_validation


1. validate_password(password, user=None, password_validators=None)
Проверяет пароль. Если все валидаторы считают пароль действительным, возвращается None.
2. password_changed(password, user=None, password_validators=None)
Сообщает всем валидаторам, что пароль быз изменен. Следует вызывать после успешного изменения пароля.
3. password_validators_help_texts(password_validators=None)
Возвращает список справочных текстов всех валидаторов. Они обьясняют пользователю требования к паролю.
4. password_validators_help_text_html(password_validators=None)
То же что и password_validators_help_texts, но в HTML.
5. get_password_validators(validator_config)
Возвращает набор обьектов валидатора из AUTH_PASSWORD_VALIDATORS.
"""


# Кастомный валидатор
class CustomValidator:
    def __init__(self, min_length) -> None:
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                'Минимальная длина пароля %(min_length)d символов.',
                code='password_too_short',
                params={'min_length': self.min_length}
            )
        
    def get_help_text(self):
        return 'Пароль должен содержать минимум %(min_length)d символов.' % {'min_length': self.min_length}


# Увеличение итераций алгоритма
from django.contrib.auth.hashers import PBKDF2PasswordHasher
class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    iterations = PBKDF2PasswordHasher.iterations + 1000


"""
- По умолчанию Django использует PBKDF2 с хешем SHA256. для системы хранения паролей.
- password = '<algotithm>$<iteraitions>$<salt>$<hash>' (алгоритм хеширования, 
кол-во обработок хеша, соль (случайное натуральное число), хеш пароля).
- Модель пользователя нужно создать в начале проекта.
- Вместо прямого обращения к User, следует ссылаться на get_user_model() или settings.AUTH_USER_MODEL.


# Создание пользователя
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
>>> user.last_name = "Lennon"
>>> user.save()


# Изменение пароля
>>> user.set_password('pass2')
>>> user.save()
# Смена пароля приводит к выходу пользователя из всех сеансов.


# Аутентификация пользователя
>>> from django.contrib.auth import authenticate
>>> us = authenticate(username='user1', password='pass')
>>> us
>>> us = authenticate(username='user1', password='pass2')
>>> us
<User: user1>


Разрешения


# Django имеет встроенную систему разрешений. Она позволяет назначить разрешения конкретным пользователям и группам пользователей.
# Методы ModelAdmin: has_view_permission(), has_add_permission(), has_change_permission(), has_delete_permission().
>>> myuser.groups.set([group_list])
>>> myuser.groups.add(group, group, ...)
>>> myuser.groups.remove(group, group, ...)
>>> myuser.groups.clear()
>>> myuser.user_permissions.set([permission_list])
>>> myuser.user_permissions.add(permission, permission, ...)
>>> myuser.user_permissions.remove(permission, permission, ...)
>>> myuser.user_permissions.clear()


# Создание разрешений
>>> from django.contrib.contenttypes.models import ContentType
>>> from django_manual.models import Animal
>>> content_type = ContentType.objects.get_for_model(Animal)
>>> permission = Permission.objects.create(code_name='can_publish', name='can publish posts', content_type=content_type)
>>> permission = Permission.objects.create(codename='can_publish', name='can publish posts', content_type=content_type)


# Кеширование разрешений происходит после первого получения
>>> from django.contrib.auth.models import Permission, User
>>> from django.contrib.contenttypes.models import ContentType
>>> from django.shortcuts import get_object_or_404
>>> from django_manual.models import Animal
>>> def user_gains_perms(request, user_id):
>>>     user = get_object_or_404(User, pk=user_id)
>>>     user.has_perm('django_manual.change_animal') # False
>>>     content_type = ContentType.objects.get_for_model(Animal)
>>>     permission = Permission.objects.get(codename='change_animal', content_type=content_type)
>>>     user.user_permissions.add(permission)
>>>     user.has_perm('django_manual.change.animal') # False
>>>     user = get_object_or_404(User, pk=user_id)
>>>     user.has_perm('django_manual.change_animal') # True


# Вход в систему. Для этого нужен аутентифицированный пользователь, HttpRequest.
# login() сохраняет id пользователя в сеансе.
>>> from django.contrib.auth import authenticate, login
>>> def my_view(request):
>>>     username = request.POST["username"]
>>>     password = request.POST["password"]
>>>     user = authenticate(request, username=username, password=password)
>>>     if user is not None:
>>>         login(request, user)
>>>         # Redirect to a success page.
>>>     else:
>>>         # Return an 'invalid login' error message.


# Выход из системы.
>>> from django.contrib.auth import logout
>>> def logout_view(request):
>>>     logout(request)
"""


class BaseBackend:
    """
    Базовый класс, предоставляющий реализации по умолчанию для всех необходимых методов.
    По умолчанию отклоняет пользователя и не предоставляет разрешений.
    """

    def authenticate(self, request, **kwargs):
        return None

    def get_user(self, user_id):
        return None

    def get_user_permissions(self, user_obj, obj=None):
        return set()

    def get_group_permissions(self, user_obj, obj=None):
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
        }

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.gettrtun_all_permissions(user_obj, obj=obj)


UserModel = get_user_model()


class ModelBackend(BaseBackend):
    """
    Механизм аутентификации по умолчанию. Аутентифицируется 
    с помощью id пользователя (USERNAME_FIELD по умолчанию) и пароля.
    Также обрабатывает модель разрешений по умолчанию для User и PermissionsMixin.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Пытается пройти аутентификацию username с password с помощью check_password().
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        """
        Разрешено ли пользователю проходить аутентификацию.
        """
        return getattr(user, "is_active", True)

    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field("groups")
        user_groups_query = "group__%s" % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = "_%s_perm_cache" % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, "_get_%s_permissions" % from_name)(user_obj)
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(
                user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms}
            )
        return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Возвращает набор строк разрешений, которые имеет user_obj.
        """
        return self._get_permissions(user_obj, obj, "user")

    def get_group_permissions(self, user_obj, obj=None):
        """
        Возвращает набор строк разрешений, которые имеет user_obj в группах.
        """
        return self._get_permissions(user_obj, obj, "group")

    def get_all_permissions(self, user_obj, obj=None):
        """
        Возвращает набор строк разрешений, которые имеет user_obj в группах и лично.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, "_perm_cache"):
            user_obj._perm_cache = super().get_all_permissions(user_obj)
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        """
        Имеет ли user_obj разрешение perm.
        """
        return user_obj.is_active and super().has_perm(user_obj, perm, obj=obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Имеет ли user_obj разрешения в приложении app_label.
        """
        return user_obj.is_active and any(
            perm[: perm.index(".")] == app_label
            for perm in self.get_all_permissions(user_obj)
        )

    def with_perm(self, perm, is_active=True, include_superusers=True, obj=None):
        """
        Возвращает всех активных пользователей у которых есть разрешения.
        """
        if isinstance(perm, str):
            try:
                app_label, codename = perm.split(".")
            except ValueError:
                raise ValueError(
                    "Permission name should be in the form "
                    "app_label.permission_codename."
                )
        elif not isinstance(perm, Permission):
            raise TypeError(
                "The `perm` argument must be a string or a permission instance."
            )

        if obj is not None:
            return UserModel._default_manager.none()

        permission_q = Q(group__user=OuterRef("pk")) | Q(user=OuterRef("pk"))
        if isinstance(perm, Permission):
            permission_q &= Q(pk=perm.pk)
        else:
            permission_q &= Q(codename=codename, content_type__app_label=app_label)

        user_q = Exists(Permission.objects.filter(permission_q))
        if include_superusers:
            user_q |= Q(is_superuser=True)
        if is_active is not None:
            user_q &= Q(is_active=is_active)

        return UserModel._default_manager.filter(user_q)

    def get_user(self, user_id):
        """
        Возвращает пользователя, если проверка пользователя прошла успешно.
        """
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class AllowAllUsersModelBackend(ModelBackend):
    """
    Не отклоняет неактивных пользователей.
    """
    def user_can_authenticate(self, user):
        return True


class RemoteUserBackend(ModelBackend):
    """
    Внешнаяя аутентификация с использованием имен пользователей в формате
    request.META['REMOVE_USER'].
    Должен использоваться вместе с RemoteUserMiddleware.
    """

    """
    Создается ли пользовательский обьект, если он еще не находится в БД.
    """
    create_unknown_user = True

    def authenticate(self, request, remote_user):
        """
        Имя пользователя remote_user - доверенное. 
        Возвращает обьект пользователя с заданным именем пользователя, 
        создавая новый обьект пользователя, если create_unknown_user=True.
        Возвращает None, если create_unknown_user=False и обьект не найден в БД.
        """
        if not remote_user:
            return
        created = False
        user = None
        username = self.clean_username(remote_user)

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(
                **{UserModel.USERNAME_FIELD: username}
            )
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass

        # RemovedInDjango50Warning: When the deprecation ends, replace with:
        #   user = self.configure_user(request, user, created=created)
        if func_supports_parameter(self.configure_user, "created"):
            user = self.configure_user(request, user, created=created)
        else:
            warnings.warn(
                f"`created=True` must be added to the signature of "
                f"{self.__class__.__qualname__}.configure_user().",
                category=RemovedInDjango50Warning,
            )
            if created:
                user = self.configure_user(request, user)
        return user if self.user_can_authenticate(user) else None

    def clean_username(self, username):
        """
        Выполняет очистку имени пользователя.
        """
        return username

    def configure_user(self, request, user, created=True):
        """
        Настраивает пользователя при каждой попытке аутентификации.
        """
        return user


class AllowAllUsersRemoteUserBackend(RemoteUserBackend):
    """
    Не отклоняет неактивных пользователей.
    """
    def user_can_authenticate(self, user):
        return True


class BaseUserManager(models.Manager):
    """
    Базовый менеджер.
    При переопределении обычно добавляются create_user(), create_superuser().
    """

    @classmethod
    def normalize_email(cls, email):
        """
        Нормализует эпочту нижним регистром второй части эпочты.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Устарело с 4.2 версии.
        Возращает случайный пароль.
        """
        warnings.warn(
            "BaseUserManager.make_random_password() is deprecated.",
            category=RemovedInDjango51Warning,
            stacklevel=2,
        )
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        """Извлекает экземпляр пользователя, используя значение USERNAME_FIELD"""
        return self.get(**{self.model.USERNAME_FIELD: username})


class UserManager(BaseUserManager):
    """
    Менеджер для модели User с полями: username, email, is_staff, is_active, 
    is_superuser, last_login, date_joined.
    """

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Создает, сохраняет и возвращает User.
        Принимает все обязательные поля.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        То же что и create_user, но is_staff=True, is_superuser=True.
        Принимает все обязательные поля.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        """
        Возвращает пользователей имеющих данное разрешение.
        is_active для получения всех активных или неактивных пользователей.
        include_superusers включать ли is_superuser.
        """
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class AbstractBaseUser(models.Model):
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Возвращает значение поля USERNAME_FIELD"""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        """Нормализует имя пользователя, вызывая normalize_username(). При переопределении обязательно super() для сохранения нормализации."""
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        # TODO что это и зачем
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """Только для чтения. Это способ различения User и AnonymousUser."""
        return False

    @property
    def is_authenticated(self):
        """Только для чтения. Это способ узнать аутентифицирован ли пользователь."""
        return True

    def set_password(self, raw_password):
        """Устанавливает пароль пользователя в заданную необработанную строку, обеспечивая хеширование пароля."""
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """Возвращает True, если необработанная строка является корректным паролем."""

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        """
        check_password - функция сравнения текстового пароля и хешированного пароля.
        """
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        """Помечает пользователя как не имеющего установленного пароля."""
        """
        make_password() - создает хешированный пароль.
        """
        self.password = make_password(None)

    def has_usable_password(self):
        """Возвращает False если пароль является результатом set_unusable_password()."""
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        # TODO Что это и как работает. Что такое HMAC
        """Возвращает HMAC поля пароля. Используется для аннулирования сеанса при смене пароля."""
        return self._get_session_auth_hash()

    def get_session_auth_fallback_hash(self):
        """Возвращает HMAC поля пароля используя SECRET_KEY_FALLBACKS. Используется в get_user()."""
        for fallback_secret in settings.SECRET_KEY_FALLBACKS:
            yield self._get_session_auth_hash(secret=fallback_secret)

    def _get_session_auth_hash(self, secret=None):
        # TODO что это и зачем
        """"""
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            secret=secret,
            algorithm="sha256",
        ).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        # TODO Как работает
        """Применяет нормализацию Юникода NFKC к именам пользователей, чтобы визуально идентичные символы с разными кодовыми точками Юникода считались идентичными."""
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )
    

class PermissionsMixin(models.Model):
    """
    Добавляет поля и методы необходимые для Group и Permission моделей,
    использующих ModelBackend.
    """

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        """
        Возвращает список строк разрешений, которые есть у пользователя.
        Если obj передано, то возвращает разрешения пользователя для obj.
        """
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        """
        Возвращает список строк разрешений, который имеет пользователь в своих группах.
        Если obj передано, возвращает разрешения группы для obj.
        """
        return _user_get_permissions(self, obj, "group")

    def get_all_permissions(self, obj=None):
        """
        Возвращает набор строк разрешений, которые имеет пользователь. 
        Входят разрешения групп и пользователя.
        """
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Возвращает True, если у пользователя есть указанное разрешение.
        Где perm это "<app label>.<permission codename>".
        Если is_active и is_superuser равны True, то всегда возвращает True.
        Если obj передан, метод будет проверять разрешения для obj.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Возвращает True, если у пользователя есть все указанные разрешения.
        Если obj передан, то метод будет проверять разрешения для obj.
        """
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Возвращает True, если у пользователя есть разрешения в модуле app_label.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)
    

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    Абстрактный базовый класс, реализующий функциональную модель пользователя 
    с разрешениями.
    """

    # Валидатор полей, допускающий сиволы Юникода, помимо @,.,+,-,_.
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    # Имя поля эпочты. Это возвращает get_email_field_name()
    EMAIL_FIELD = "email"
    # Имя поля, которое используется в качестве идентификатора (username, email)
    USERNAME_FIELD = "username"
    # Список имен полей при createsuperuser (password и USERNAME_FIELD постфактум)
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        """Нормализует эпочту. При переопределении обязательно super()."""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Возвращает имя пользователя."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправляет email пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



class User(AbstractUser):
    """
    Рекомендуется настроить собственную модель пользователя, 
    даже если достаточно модели по умолчанию.
    Это идентичная модель пользователя по умолчанию, 
    но ее можно будет настроить в будущем.
    
    При изменении модели пользователя ее нужно обновить в ModelAdmin. 
    """
    pass
