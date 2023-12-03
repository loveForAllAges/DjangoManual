
"""
Middleware - промежуточное программное обеспечение.
"""


# Middleware в виде функции
from typing import Any


def simple_middleware(get_response):
    # Приинмает get_response обьект и возвращает middleware (вызываемый обьект, который принимает запрос и возвращает ответ, как и представление).

    def middleware(request):
        # Код до представления
        response = get_response(request)
        # Код после вызова представления
        return response
    
    return middleware


# Middleware в виде класса
class SimpleMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        # Код до представления
        # print('OK')
        response = self.get_response(request)
        # Код после вызова представления
        return response
    
    # def process_view(request, view_func, view_args, view_kwargs):
    #     """
    #     request: HttpRequest обьект.
    #     view_func: функция Python, которая будет вызвана.
    #     view_args: список позиционных аргументов, которые будут переданы в представление.
    #     view_kwargs: словарь аргументов ключевых слов, которые будут переданы в представление.

    #     process_view() вызывается перед тем как вызывается представление.
    #     Возвращает HttpRequest обьект или None. Если None, то обработка запроса продолжится в поисках любого другого process_view().
    #     Если возвращает обьект, то другие middleware вызваны не будут.
    #     """
    #     pass

    # def process_exception(request, exception):
    #     """
    #     request: HttpRequest обьект.
    #     exception: Exception обьект, созданный функцией просмотра.

    #     process_exception() вызывается когда представление вызывает исключение.
    #     Возвращает HttpRequest обьект или None. Если возвращает обьект, будут применены ответ шаблона и промежуточное программное обеспечение ответа и полученный ответ будет возвращен в браузер.
    #     Иначе срабатывает обработка исключений по умолчанию.
    #     """
    #     pass

    # def process_template_response(request, response):
    #     """
    #     request: HttpResponse обьект.
    #     response: TemplateResponse обьект, возвращаемый представлением или middleware.

    #     process_template_response() вызывается после завершения выполнения представления.
    #     Должен возвращать обьект ответа, реализующий render метод. Может создать и вернуть совершенно новое TemplateResponse.
    #     """
    #     pass
