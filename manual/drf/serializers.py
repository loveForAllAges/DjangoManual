from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.validators import (
    UniqueTogetherValidator, UniqueForYearValidator
)

from .models import Task, Subtask, Album, Track, Post, DataPoint

from django.contrib.auth.models import User
from django.utils import timezone

import re

import time


def max_len_32(value):
    if len(value) > 32:
        raise serializers.ValidationError('Max len 32')


class PostSerialzer2(serializers.Serializer):
    body = serializers.CharField(max_length=128, validators=[max_len_32])

    class Meta:
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['body', 'id']
            )
        ]

    def validate_body(self, value):
        if 'a' in value:
            raise serializers.ValidationError('А запрещено')
        return value

    def validate(self, attrs):
        if attrs['body']:
            raise serializers.ValidationError('Тест ошибка')
        return attrs

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class ProfileSerializer():
    # Test class
    pass


class Profile():
    # Test class
    pass


class TestUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

    def create(self, validated_data):
        # Создание пользователя с вложенным обьектом профиля.
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # Обновление пользователя с вложенным обьектом профиля.
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        profile.is_premium_member = profile_data.get('is_premium_member', 
                                                     profile.is_premium_member)
        profile.save()
        return instance


class CustomListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        posts = [Post(**item) for item in validated_data]
        return Post.objects.bulk_create(posts)
    
    def update(self, instance, validated_data):
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret


class CustomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    class Meta:
        # Кастомный класс, который используется при many=True.
        list_serializer_class = CustomListSerializer


class HighScoreSerializer(serializers.BaseSerializer):
    # Сериализатор только для чтения.
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }

    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')

        if not score:
            raise serializers.ValidationError({
                'score': 'Это обязательное поле.'
            })
        
        return {
            'score': int(score),
            'player_name': player_name
        }

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_representation(self, instance):
        output = {}
        for attribute_name in dir(instance):
            attribute = getattr(instance, attribute_name)
            if attribute_name.startswith('_'):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [
                    self.to_representation(item) for item in attribute
                ]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {
                    str(key): self.to_representation(value)
                    for key, value in attribute.items()
                }
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)
        return output


class UserSerializer3(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_days(self, obj):
        return 10


class Color:
    def __init__(self, red, green, blue):
        assert(red >= 0 and green >= 0 and blue >= 0)
        assert(red < 256 and green < 256 and blue < 256)
        self.red, self.green, self.blue = red, green, blue


#  Кастомное поле цвета RGB.
class ColorField(serializers.Field):
    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected a string, but got {input_type}',
        'incorrect_format': 'Incorrect format. Expected `rgb(#,#,#)`.',
        'out_of_range': 'Value out of range. Must be between 0 and 255.'
    }

    def to_representation(self, value):
        return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)
    
    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
            self.fail('incorrect_format')

        data = data.strip('rgb(').rstrip(')')
        red, green, blue = [int(col) for col in data.split(',')]

        if any([col > 255 or col < 0 for col in (red, green, blue)]):
            self.fail('out_of_range')

        return Color(red, green, blue)


# Кастомное поле, которое можно использовать для представления имени класса 
# сериализуемого обьекта.
class ClassNameField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        return value.__class__.__name__


class CoordinateField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "x": value.x_coordinate,
            "y": value.y_coordinate
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "x_coordinate": data["x"],
            "y_coordinate": data["y"],
        }
        return ret


# Используя кастомное поле и source='*', можно предоставит вложенное 
# представление пары координат.
class DataPointSerializer(serializers.ModelSerializer):
    coordinates = CoordinateField(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']


class NestedCoordinateSerializer(serializers.Serializer):
    x = serializers.IntegerField(source='x_coordinate')
    y = serializers.IntegerField(source='y_coordinate')


# То же самое, но с использованием вложенного сериализатора.
class DataPointSerializer(serializers.ModelSerializer):
    coordinates = NestedCoordinateSerializer(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


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


class AlbumSerializer2(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = '__all__'


class AlbumSerializer3(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'

class AlbumSerializer4(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = '__all__'


class AlbumSerializer5(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='id'
    )

    class Meta:
        model = Album
        fields = '__all__'


class AlbumSerializer6(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(
        view_name='album-detail',
    )

    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        exclude = ['album']


class AlbumSerializer7(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'


# Записываемый вложенный сериализатор
class AlbumSerializer8(serializers.HyperlinkedModelSerializer):
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
    

# Реляционное поле поле для сериализации трека в пользовательское строковое 
# представление, используя порядок, название и продолжительность.
class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(value.duration))
        return 'Track %d: %s (%s)' % (value.order, value.name, duration)


# class AlbumSerializer9(serializers.ModelSerializer):
#     tracks = TrackListingField(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']


# Кастомное поле с гиперссылкой.
class UserHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'user-detail'
    queryset = User.objects.all()

    # Используется для сопоставления экземпляра обьекта с его URL.
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'organization_slug': obj.organization.slug,
            'customer_pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    # Сопоставляет входящие URL обратно с обьектом, который он представляет.
    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['organization_slug'],
           'pk': view_kwargs['customer_pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
    

# Пример валидатора UniqueTogetherValidator.
class ExampleSerializer(serializers.Serializer):
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['field1', 'field2']
            )
        ]


# Пример валидатора UniqueForYearValidator.
class ExampleSerializer(serializers.Serializer):
    class Meta:
        validators = [
            UniqueForYearValidator(
                queryset=Post.objects.all(),
                field='slug',
                date_field='published'
            )
        ]


class ExampleSerializer(serializers.Serializer):
    # Пример валидатора CurrentUserDefault.
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # Пример валидатора CreateOnlyDefault.
    created_at = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now)
    )