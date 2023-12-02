from django.core.mail import send_mail, send_mass_mail, EmailMessage


"""
Раздел: Sending email (Отправка электронной почты)


Почта отправляется с использованием хоста SMTP и порта, указанных в настройках EMAIL_HOST и EMAIL_PORT.
Параметры EMAIL_HOST_USER и EMAIL_HOST_PASSWORD используются для аутентификации на SMTP-сервере.
Параметры EMAIL_USE_TSL и EMAIL_USE_SSL определяют, используется ли безопасное соединение.
"""


"""
send_email(
    subject: str,
    message: str,
    from_email: str, # По умолчанию DEFAULT_FROM_EMAIL.
    recipient_list: list, # список email адресов.
    fail_silently=False: bool, # возникнет ли ошибка.
    auth_user=None: str, # имя пользователя для аутентификации на SMTP-сервере. По умолчанию EMAIL_HOST_USER.
    auth_password=None: str, # пароль для аутентификации на SMTP-сервере. По умолчанию EMAIL_HOST_PASSWORD.
    connection=None, # доп. сервер почты для отправки.
    html_message=None # html сообщение
) -> Integer # Кол-во успешно отправленных сообщений

Отправляет письмо.
"""


def send_email_func():
    send_mail(
        'Subject here',
        'Message',
        'from@gmail.com',
        ['to@example.com',],
        fail_silently=False
    )


"""
send_mass_mail(
    datatuple: tuple, # кортеж элементов (subject, message, from_email, recipient_list).
    fail_silently=False, # то же что и в send_mail().
    auth_user=None, # то же что и в send_mail().
    auth_password=None, # то же что и в send_mail().
    connection=None
) -> Integer # Кол-во успешно отправленных сообщений

Предназначено для обработки массовой рассылки по эл. почте.
"""

def send_mass_mail_func():
    message1 = (
        "Subject here",
        "Here is the message",
        "from@example.com",
        ["first@example.com", "other@example.com"],
    )
    message2 = (
        "Another Subject",
        "Here is another message",
        "from@example.com",
        ["second@test.com"],
    )
    send_mass_mail((message1, message2), fail_silently=False)


"""
Отличие между send_mail() и send_mass_mail():
send_mail() каждый раз при выполнении открывает соединение с почтовым сервером,
а send_mass_mail() использует одно соединение.
"""


"""
mail_admins(
    subject,
    message,
    fail_silently=False,
    connection=None,
    html_message=None
)

Предназначен для отправки письма администраторам сайта, как в ADMINS настройках.
Добавляет к теме префикс параметр EMAIL_SUBJECT_PREFIX ('[Django]').
Заголовок письма будет SERVER_EMAIL.
"""


"""
mail_managers(
    subject,
    message,
    fail_silently=False,
    connection=None,
    html_message=None
)

Аналогичен mail_admins(), за исключением того, что отправляет письмо менеджерам сайта, как в MANAGERS настройках.
"""


"""
EmailMessage


Вышеперечисленные фукнции отправки писем используют класс EmailMessage.

Параметры:
    - subject - тема письма.
    - body - основной текст.
    - from_email - адрес отправителя. По умолчанию DEFAULT_FROM_EMAIL.
    - to - список или кортеж адресов получателей.
    - bcc - список адресов, используемых в заголовке письма.
    - connection - экземпляр серверной части почты. Создает одно соединение для нескольких сообщений. 
    - attachments - список вложений к сообщению.
    - headers - словарь доп. заголовков для сообщения.
    - cc - список адресов получателей в заголовке "Копия" письма.
    - reply_to - список адресов получателей в заголовке "Ответить" письма.
Методы:
    - send(fail_silently=False) - отправляет сообщение.
    - message() - создает django.core.mail.SafeMIMEText или django.core.mail.SafeMIMEMultipart обьект, содержащий отправляемое сообщение.
    - recipients() - возвращает списко всех получателей.
    - attach() - создает новое вложение файла и добавляет его в сообщение.
    - attach_file() - создает новое вложение, используя файл из файловой системы.
"""

def mail_class():
    email = EmailMessage(
        'Hello',
        'Body',
        'from@example.com',
        ['to1@example.com',],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
    )


"""
Серверная часть SMTP

backends.smtp.EmailBackend(
    host=None, # EMAIL_HOST
    port=None, # EMAIL_PORT
    username=None, # EMAIL_HOST_USER
    password=None, # EMAIL_HOST_PASSWORD
    use_tls=None, # EMAIL_USE_TLS
    fail_silently=False,
    use_ssl=None, # EMAIL_USE_SSL
    timeout=None, # EMAIL_TIMEOUT
    ssl_keyfile=None, # EMAIL_SSL_KEYFILE
    ssl_certfile=None, # EMAIL_SSL_CERTFILE
    **kwargs
)
"""


"""
Консольный бэкенд


Для разработки.
Вместо отправки реальных писем они выводятся в консоль.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
"""


"""
Файловый сервер


Для разработки.
Серверная часть файла записывает эл. письма в файл.

EMAIL_FILE_PATH - Каталог файлов.
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/tmp/app-messages" 
"""


"""
Серверная часть в памяти


Для разработки.
Серверная часть хранит сообщения в спец. атрибуте модуля django.core.mail.
Тесты используют этот бэкенд для тестирования.

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
"""

"""
Фиктивный бэкэнд


Для разработки.
Фиктивный бэкенд ничего не делает.

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
"""


"""
Примеры


from django.core import mail

connection = mail.get_connection()

connection.open()

email1 = mail.EmailMessage(
    "Hello",
    "Body goes here",
    "from@example.com",
    ["to1@example.com"],
    connection=connection,
)
email1.send()

email2 = mail.EmailMessage(
    "Hello",
    "Body goes here",
    "from@example.com",
    ["to2@example.com"],
)
email3 = mail.EmailMessage(
    "Hello",
    "Body goes here",
    "from@example.com",
    ["to3@example.com"],
)

connection.send_messages([email2, email3])
connection.close()
"""