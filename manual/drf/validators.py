"""
rest_framework.validators

UniqueValidator(
    queryset: Набор запросов в отношении которого должна применяться уникальность,
    message: Сообщение об ошибке при неудачной проверке,
    lookup: Поиск для нахождения существующего экземпляра с проверямым значением. По умолчанию exact
)
Валидатор используется для ограничения unique=True.

Пример:
`
slug = SlugField(validators=[UniqueValidator(queryset=Model.objects.all())])
`



UniqueTogetherValidator(
    queryset:,
    fields: список или кортеж имен полей, которые должны быть уникальны,
    message
)
Валидатор используется для наложения ограничений unique_together на экземпляры модели.

Пример:
`
class ExampleSerializer(serializers.Serializer):
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Model.objects.all(),
                fields=['field1', 'field2']
            )
        ]
`



UniqueForDateValidator()
UniqueForMonthValidator()
UniqueForYearValidator(
    queryset,
    field,
    date_field: имя поля, которое будет использоваться для определения диапазона дат для уникальности,
    message
)

Пример:
`
class ExampleSerializer(serializers.Serializer):
    class Meta:
        validators = [
            UniqueForYearValidator(
                queryset=BlogPostItem.objects.all(),
                field='slug',
                date_field='published'
            )
        ]
`



CurrentUserDefault()
Класс по умолчанию, который может быть использован для представления текущего пользователя. 
Чтобы использовать его, request должен быть предоставлен как часть контекстного словаря при инстанцировании сериализатора.

Пример:
`
owner = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
`



CreateOnlyDefault()
Класс по умолчанию, который можно использовать для только для установки аргумента по умолчанию во время операций создания.
При обновлении поле опускается.

Пример:
`
created_at = serializers.DateTimeField(
    default=serializers.CreateOnlyDefault(timezone.now)
)
`


Создание валидатора
def even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even number.')


class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            message = 'This field must be a multiple of %d.' % self.base
            raise serializers.ValidationError(message)
"""