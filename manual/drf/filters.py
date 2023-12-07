"""
rest_framework.filters



DjangoFilterBackend()

pip install django-filter

INSTALLED_APPS = [
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

Пример:
class AlbumListAPI(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['artist', 'id']

Запрос: 
http://example.com/api/products?artist=clothing&id=1



SearchFilter()
Поддерживает простой поиск по одному параметру запроса.
Применяется, если у представления установлен атрибут search_fields.

Пример:
class AlbumListAPI(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['artist', 'id']
    search_fields = ['artist', 'name', 'tracks__title']

Запрос:
http://127.0.0.1:8000/api/album?search=art%201&id=1

Поведение поиска может быть задано путем добавления префикса к именам полей в search_fields одним из следующих символов:
^ - istartswith (начинается с поиска)
= - iexact (точные совпадения)
$ - iregex (regex-поиск)
@ - search (полнотектовый поиск)

Например: search_fields = ['=username', '=email']

По умолчанию параметр поиска называется 'search', можно переопределить с помощью параметра SEARCH_PARAM


OrderingFilter()
Поддерживает простое упорядочивание результатов, управляемое параметрами запроса.
По умолчанию параметр запроса называется 'ordering', но это можно переопределить с помощью ORDERING_PARAM.
Для сортировки по убыванию необходимо добавить префикс '-'.

Пример:
class AlbumListAPI(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'name']

Запрос:
http://127.0.0.1:8000/api/album?ordering=-id

Если у представления есть атрибут ordering, то он будет использоваться в качестве упорядочивания по умолчанию.
Пример:
class AlbumListAPI(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    ordering = ['-id']


    
Создание собственной фильтрации:
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
"""

