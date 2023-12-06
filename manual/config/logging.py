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