"""
rest_framework.permissions


Политика разрешений по умолчанию может быть установлена глобально с помощью параметра DEFAULT_PERMISSION_CLASSES. 
Например.
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
]

Если этот параметр не указан, то по умолчанию он разрешает неограниченный доступ:
'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
]

Вы также можете установить политику аутентификации на основе каждого представления или каждого набора представлений, используя представления на основе класса APIView.
permission_classes = [IsAuthenticated]

При условии наследования от rest_framework.permissions.BasePermission, разрешения могут быть составлены с использованием стандартных побитовых операторов Python.
Например, IsAuthenticatedOrReadOnly может быть записано:
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


        
AllowAny()
Разрешает неограниченный доступ



IsAuthenticated()
Запрещает разрешение не прошедшему аутентификацию пользователю



IsAdminUser()
Запрещает разрешение любому пользователю если user.is_staff не является True



IsAuthenticatedOrReadOnly()
Разрешает аутентифицированным пользователям выполнять любые запросы, а анонимным только чтение.



DjangoModelPermissions()
Это разрешение должно применяться только к представлениям, имеющим свойство .queryset или метод get_queryset(). 
Авторизация будет предоставлена только в том случае, если пользователь аутентифицирован и имеет соответствующие разрешения модели.



DjangoModelPermissionsOrAnonReadOnly()
Аналогичен DjangoModelPermissions, но также позволяет неаутентифицированным пользователям иметь доступ к API только для чтения.



DjangoObjectPermissions()
Как и DjangoModelPermissions, это разрешение должно применяться только к представлениям, имеющим свойство .queryset или метод .get_queryset(). 
Разрешение будет предоставлено только в том случае, если пользователь аутентифицирован и имеет соответствующие разрешения на объект и соответствующие разрешения на модель.



Чтобы реализовать пользовательское разрешение, переопределите BasePermission и реализуйте один или оба из следующих методов:
.has_permission(self, request, view)
.has_object_permission(self, request, view, obj)
Методы должны возвращать True, если запрос должен получить доступ, и False в противном случае.



Примеры
Ниже приведен пример класса разрешения, который проверяет IP-адрес входящего запроса по списку блокировки и отклоняет запрос, если IP-адрес был заблокирован.
from rest_framework import permissions

class BlocklistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        return not blocked        
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
