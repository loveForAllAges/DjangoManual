from django.core.checks import Error, register, Tags


"""
Раздел: System check framework (Фреймворк проверки системы)


Фреймворк системной проверки обнаруживает распросраненные проверки и дает подсказки по их устранению.
Платформа расширяема. Проверки запускаются с помощью команды python manage.py check.


TODO
Список всех проверок:
https://docs.djangoproject.com/en/5.0/ref/checks/
"""


# Написание собственных проверок. Пример функции проверки заглушки.
@register() # Маркировка проверок.
def example_check(app_configs, **kwargs):
    # app_config - список приложений для проверки. 
    # Если None, то проверка для всех приложений.
    errors = []
    # check logic
    check_failed = False
    checked_object = ''
    # ...
    # end check logic
    if check_failed:
        errors.append(
            Error(
                'an error',
                hint='A hint.',
                obj=checked_object,
                id='myapp.E001',
            )
        )
    # Возвращает список сообщений (CheckMessage) или пустой список.
    return errors


@register(Tags.compatibility)
def my_check(app_configs, **kwargs):
    # Выполнение проверок и сбор ошибок
    errors = []
    # end
    return errors


# Регистрация проверок развертывания для производственных настроек.
@register(Tags.security, deploy=True)
def my_check(app_configs, **kwargs):
    pass
