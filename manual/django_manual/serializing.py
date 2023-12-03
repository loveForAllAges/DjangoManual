"""
Раздел: Serializing Django objects (Сериализация обьектов)


Сериализация подмножества полей:
serializers.serialize('xml', SomeModel.objects.all(), fields=['name', 'size'])

Десериализация данных:
serializers.deserialize('xml', data)

Сериализатор JSON использует django.core.serializers.json.DjangoJSONEncoder для кодирования.

serializer.serialize(
    indent, # 
    use_natural_foreign_keys, # Использовать ли метод natural_key() для сериализации любой ссылки внешнего ключа.
    user_natural_primary_keys # Предоставлять ли первичный ключ в сериализованных данных обьекта.
)
"""

from django.core import serializers
from django_manual.models import Author


objs = Author.objects.all()
data = serializers.serialize('json', objs)

"""
"""