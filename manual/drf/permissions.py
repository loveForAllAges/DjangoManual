from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS



class CustomerAccessPermission(permissions.BasePermission):
    # Изменить сообщение об ошибке
    message = 'Сообщение об ошибке'


Blocklist = '' # Тестовая модель


# Проверяет IP-адрес входящего запроса по списку блокировки и отклоняет запрос, 
# если IP-адрес был заблокирован.
class BlocklistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        return not blocked


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
