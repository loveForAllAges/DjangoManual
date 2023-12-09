from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Task, Subtask, Album, Track
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



"""
Опции:
allow_blank - Допустимо пустое значение
trim_whitespace - Обрезание крайних пробелов
path - Абсолютный путь к каталогу
match - рег. Выражение для фильтрации имен файлов
recursive - Включение всех подкаталогов путей
protocol - Ограничение допустимых входов с указанным протоколом (both, IPv4, IPv6)
unpack_ipv4 - Распаковка IPv4 адресов
max_digits - Максимальное количество цифр в числе
decimal_places - Количество знаков после запятой
coerce_to_string - Возвращать в виде строки
format - Формат вывода
input_formats - Список строк того, в каком формате может быть ввод даты
default_timezone - Определение часового пояса
choices - список допустимых значений или картежей
html_cutoff - Максимальное количество выводимых вариантов 
allow_empty_file - Разрешен пустой файл
use_url - Выходные данные в формате URL
child - экземпляр поля для проверки обьектов в списке
binary - Вывод и проверка строки в кодировке JSON
encoder - JSON-кодер для сериализации входного обьекта
method_name - Имя метода сериализатора, который будет вызван

BooleanField()
CharField(max_length, min_length, allow_blank, trim_whitespace)
EmailField(max_length, min_length, allow_blank)
RegexField(regex, max_length, min_length, allow_blank)
SlugField(max_length, min_length, allow_blank)
URLField(max_length, min_length, allow_blank)
UUIDField(format)
FilePathField(path, match, recursive, allow_files, allow_folders, required, **kwargs)
IPAddressField(protocol, unpack_ipv4, **options)
IntegerField(max_value, min_value)
FloatField(max_value, min_value)
DecimalField(max_digits, decimal_places, coerce_to_string, max_value, min_value)
DateTimeField(format, input_formats, default_timezone)
DateField(format, input_formats)
TimeField(format, input_formats)
DurationField(max_value, min_value)
ChoiceField(choices)
MultipleChoiceField(choices)
FileField(max_length, allow_empty_file, use_url)
ImageField(max_length, allow_empty_file, use_url)
ListField(child, allow_empty, min_length, max_length)
DictField(child, allow_empty)
HStoreField(child, allow_empty)
JSONField(binary, encoder)
ReadOnlyField()
- Возвращает значение поля без модификации
HiddenField()
- Принимает значение вызываемого поля, а не значение пользовательского ввода
ModelField(model_field)
- Предназначен для внутреннего использования (Привязывается к любому полю модели), но при необходимости может быть использован API

SerializerMethodField(method_name)
- Доступно только для чтения. Вызывает метод класса сериализатора. Используется для добавления данных в сериализованное представление

Пример:
`
class UserSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_days(self, obj):
        return 10
`


StringRelatedField()
Описание:
Возвращает обьекты в формате, который указан в __str__ в модели обьекта. 
Доступно только для чтения.

Пример:
`
class AlbumSerializer(ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = '__all__'
`



PrimaryKeyRelatedField(
    queryset: набор запросов для поиска обьекта модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить read_only=True, 
    many,
    allow_null,
    pk_field: для управления сериализацией/десериализацией значения первичного ключа. Например, pk_field=UUIDField(format='hex')
)
Описание:
Возвращает обьекты в формате первичного ключа.
Доступно для чтения-записи (изменить read_only).

Пример:
`
class AlbumSerializer(ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'
`



HyperlinkedRelatedField(
    view_name: имя представления для цели отношения,
    queryset, 
    many,
    allow_null,
    lookup_field: Поле цели для поиска, которое соответствует именованному аргменту URL. По умолчанию pk,
    lookup_url_kwarg: Имя именованного аргумента в URL conf, которое соответствует полю поиска,
    format: если используются суффиксы формата, то поля с гиперссылками используют тот же суффикс формата для цели
)
Описание:
Возвращает список обьектов в виде ссылок на обьекты.
Доступно для чтения-записи (изменить read_only).

Пример:
`
class AlbumSerializer(ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='track-detail')

    class Meta:
        model = Album
        fields = '__all__'
`



SlugRelatedField(
    slug_field: поле цели для представления обьекта,
    queryset,
    many,
    allow_null
)
Описание:
Возвращает обьекты с помощью поля цели
Доступно для чтения-записи (изменить read_only).

Пример:
`
class AlbumSerializer(ModelSerializer):
    tracks = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')

    class Meta:
        model = Album
        fields = '__all__'
`



HyperlinkedIdentityField(
    view_name: имя представления для цели отношения,
    lookup_field,
    lookup_url_kwarg,
    format
)
Описание:
Применяется как отношение идентичности

Не отработало!

Пример:
`
class AlbumSerializer(HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = '__all__'
`



Вложенные отношения
Пример:
`
class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        exclude = ['album']


class AlbumSerializer(HyperlinkedModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'
`



Записываемые вложенные сериализаторы
Пример:
`
class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        exclude = ['album']


class AlbumSerializer(HyperlinkedModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'

    def create(self, validated_data):
        tracks = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track in tracks:
            Track.objects.create(album=album, **track)
        return album
`
"""


# def max_len_4(value):
#     if len(value) > 4:
#         raise ValidationError('Макс длина 4')
    
# def not_empty(value):
#     if not value:
#         raise ValidationError('Не пустое')


# class TaskSerializer(Serializer):
#     title = CharField(validators=[not_empty, max_len_4])


# class TaskSerializer(Serializer):
#     title = CharField()

#     def validate_title(self, value):
#         if not value:
#             raise ValidationError('не пустое')
#         if len(value) > 4:
#             raise ValidationError('не более 4 символов')
#         return value
        
#     def create(self, validated_data):
#         return Task.objects.create(**validated_data)


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(error_messages={
        'blank': 'Ошибка'
    })
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'
        # exclude = ['id']

    def validate_title(self, value):
        if "T" not in value:
            raise ValidationError('T must be')
        return value

    def create(self, validated_data):
        print('created', validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        print('updated', instance, validated_data)
        return super().update(instance, validated_data)


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        exclude = ['album']


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'

    def create(self, validated_data):
        tracks = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track in tracks:
            Track.objects.create(album=album, **track)
        return album

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

# from .models import Women


# class WomenSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Women
#         fields = "__all__"
