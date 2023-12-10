from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination, CursorPagination,
    BasePagination
)
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-id'


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
