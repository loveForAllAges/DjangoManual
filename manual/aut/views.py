
"""
Раздел: Authentication (Аутентификация).


Аутентификация проверяет является ли пользователь тем, за кого он себя выдает.
Авторизация определяет, что разрешено делать аутентифицированному пользователю.



Аннулирование сессии при смене пароля.

Если AUTH_USER_MODEL наследуется от AbstractBaseUser или реализует метод get_session_auth_hash(), то аутентифицированные сеансы будут включать хеш возвращаемый этой функцией.
Смена пароля по умолчанию PasswordChangeView обновляет сеанс новым хешем пароля, чтобы пользователь не выходил из системы после смена пароля.
Для собственной реализации использовать update_session_auth_hash(request, user) - обновляет хеш сеанса и меняет ключ сессии.



Аутентификация по умолчанию.
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']

Больший контроль:
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("change-password/", auth_views.PasswordChangeView.as_view(template_name="change-password.html")),
]



logout_then_login(request, login_url=None) - выводит пользователя из системы POST запросом и перенаправляет на страницу входа.
redirect_to_login(next, login_url=None, redirect_field_name='next') - перенаправляет на страницу входа, а затем на другой url после успешного входа.
"""
