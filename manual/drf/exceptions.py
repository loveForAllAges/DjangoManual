from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class CustomAPIException(APIException):
    status_code = 503
    default_detail = 'Custom APIException'
    default_code = 'custom_exc'
