"""
Раздел: Decorators (Декораторы).


from django.views.decorators.http import condition
Принимает две функции, чтобы определить, совпадают ли заголовки в HTTP-запросе с заголовками в ресурсе.
Если не совпадают, необходимо вычислить новую копию ресурса и вызвать обычное представление.
condition(etag_func=None, last_modified_func=None).
Декоратор устанавливает заголовки ETag и Last-Modified, если они еще не установлены и метод GET или HEAD.


Пример.
Используем модели Blog и Entry.

Если главная страница, отображающая последние записи блога, меняется только при добавлении новой записи блога, то можно определить время последнего изменения.

def latest_entry(request, blog_id):
    return Entry.objects.filter(blog=blog_id).latest('published').published

@condition(last_modified_func=latest_entry)
def front_page(request, blog_id):
    pass
    

- django.contrib.auth.decorators.login_required(redirect_field_name='next', login_url=None) - Если пользователь не вошел в систему, то редирект LOGIN_URL.
- django.contrib.auth.decorators.user_passes_test(test_func, login_url=None, redirect_field_name='next') - Запускает функцию test_func и если она возвращает False, то выполняется перенаправление на LOGIN_URL.
- django.contrib.auth.decorators.permission_required(perm, login_url=None, raise_exception=False) - проверка наличия у пользователя разрешения.
"""
