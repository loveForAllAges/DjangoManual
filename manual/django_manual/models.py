from django.db import models
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
import datetime


class Blog(models.Model):
    name = models.CharField(max_length=64)


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.datetime.now)


class Animal(models.Model):
    name = models.CharField(max_length=64)
    sound = models.CharField(max_length=32)

    def speak(self):
        return self.sound


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name
    

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


# ---


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField(auto_now_add=True)


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)


# ---


class PollManager(models.Manager):
    # Чтобы изменить вывод .all() необходимо изменить get_queryset()
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(question="AA")

    # Дополнительный метод, который можно вызвать OpinionPoll.test.with_counts().
    def with_counts(self):
        return self.annotate(num_responses=Coalesce(models.Count('response'), 0))


class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    objects = models.Manager() # Менеджер по умолчанию
    test = PollManager() # Менеджер кастомный


class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)


class TablespaceExample(models.Model):
    # Создается табличное пространство indexes
    # Поле data также генерирует индекс, но табличное пространство tables
    name = models.CharField(max_length=30, db_index=True, db_tablespace='indexes')
    data = models.CharField(max_length=255, db_index=True)
    shortcut = models.CharField(max_length=7)
    edges = models.ManyToManyField(to='self', db_tablespace='indexes')

    class Meta:
        db_tablespace = 'tables'
        indexes = [models.Index(fields=['shortcut'], db_tablespace='other_indexes')]

"""
# Model field types (Поля моделей)

1. AutoField
2. BigAutoField
3. BigIntegerField
4. BinaryField
5. BooleanField
6. CharField
7. DateField
8. DateTimeField
9. DecimalField
10. DurationField
11. EmailField
12. FileField
13. FilePathField
14. FloatField
15. GenericIPAddressField
16. ImageField
17. IntegerField
18. JSONField
19. PositiveBigIntegerField
20. PositiveIntegerField
21. PositiveSmallIntegerField
22. SlugField
23. SmallAutoField
24. SmallIntegerField
25. TextField
26. TimeField
27. URLField
28. UUIDField
29. ForeignKey
30. ManyToManyField
31. OneToOneField
32. GenetatedField

1. AutoField(**options) - целочисленное поле, автоматически увеличиваемое с каждым новым обьектом. Используется как первичный ключ.
2. BigAutoField(**options) - то же, что и AutoField, но для больших целых чисел (1 - 9223372036854775807).
3. BigIntegerField(**options) - поле для хранения больших целых чисел (-9223372036854775808 - 9223372036854775807).
4. BinaryField(max_length=None, **options) - поле для хранения бинарных данных (например, изображения или файлы).
5. BooleanField(**options) - поле для хранения булевых значений.
6. CharField(max_length=None, **options) - поле для хранения строки с фиксированной длиной.
7. DateField(auto_now=False, auto_now_add=False, **options) - поле для хранения даты (datetime).
8. DateTimeField(auto_now=False, auto_now_add=False, **options) - поле для хранения даты и времени (datetime).
9. DecimalField(max_digits=None, decimal_places=None, **options) - поле для хранения чисел с плавающей точкой (Decimal).
10. DurationField(**options) - поле для хранения длительности времени (timedelta).
11. EmailField(max_length=254, **options) - поле CharField с валидатором EmailValidator.
12. FileField(upload_to='', storage=None, max_length=100, **options) - поле для хранения файлов.
13. FilePathField(path='', match=None, recursive=False, allow_files=True, allow_folders=False, max_length=100, **options) - поле для хранения путей к файлам на сервере.
14. FloatField(**options) - поле для хранения чисел с плавающей точкой (float).
15. GenericIPAddressField(protocol='both', unpack_ipv4=False, **options) - поле для хранения IP-адресов (IPv4 или IPv6).
16. ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options) - то же, что и FileField, но для изображений.
17. IntegerField(**options) - поле для хранения целых чисел ({-2 147 483 648; 2 147 483 647}).
18. JSONField(encoder=None, decoder=None, **options) - поле для хранения данных в формате JSON.
19. PositiveBigIntegerField(**options) - то же, что и BigIntegerField, но для положительных чисел ({0; 9 223 372 036 854 775 807}).
20. PositiveIntegerField(**options) - то же, что и IntegerField, но для положительных чисел ({0; 2 147 483 647}).
21. PositiveSmallIntegerField(**options) - то же, что и SmallIntegerField, но для положительных чисел ({0; 32 767}).
22. SlugField(max_length=50, allow_unicode=False, **options) - поле для хранения slug.
23. SmallAutoField(**options) - то же, что и AutoField, но для маленьких целых чисел ({1, 32 767}).
24. SmallIntegerField(**options) - поле для хранения маленьких целых чисел ({-32 768; 32 767}).
25. TextField(**options) - поле для хранения длинных текстовых данных.
26. TimeField(auto_now=False, auto_now_add=False, **options) - поле для хранения времени (datetime.time).
27. URLField(max_length=200, **options) - поле CharField с валидатором URLValidator.
28. UUIDField(**options) - поле для хранения уникальных идентификаторов UUID (UUID).
29. ForeignKey(to_field, on_delete, **options) - поле для создания отошения многие к одному.
30. ManyToManyField(to_field, **options) - поле для создания отношения многие ко многим.
31. OneToOneField(to_field, on_delete, parent_link=False, **options) - поле для создания отношения один к одному.

32. GenetatedField(
    expression,         # Expression используется БД для автоматической установки значения поля при изменении модели. 
                        # Выражения должны быть детерминированными и ссылаться только на поля внутри модели. 
                        # Сгенерированные поля не могут ссылаться на другие сгенерированные поля.

    output_field,       # Экземпляр поля модели для определения типа данных поля.

    db_persist=None,    # Если False, то столбец действует как виртуальный и не занимает место в БД. Иначе как хранимый столбец.
                        # PostgreSQL поддерживает только постоянные столбцы.

    **kwargs
)                       # Поле, которое вычисляется на основе других полей. Это поле управляется и обновляется самой БД (GENERATED ALWAYS sql syntax).

Пример:

class Square(models.Model):
    side = models.IntegerField()
    area = models.GeneratedField(
        expression=F('side') * F('side'),
        output_field=models.BigIntegerField(),
        db_persist=True
    )
"""



"""
# Model field options (Опции полей моделей)

1. null
2. blank
3. choices
4. db_column
5. db_comment
6. db_index
7. db_tablespace
8. default
9. editable
10. error_messages
11. help_text
12. primary_key
13. unique
14. unique_for_date
15. unique_for_month
16. unique_for_year
17. verbose_name
18. validators
17. auto_now
18. auto_now_add
19. max_length
20. min_length
21. db_collation
22. max_digits
23. decimal_places
24. upload_to
25. storage
26. path
27. match
28. recursive
29. allow_files
30. allow_folders
31. protocol
32. unpack_ipv4
33. height_field
34. width_field
35. encoder
36. decoder
37. allow_unicode
38. to_field
39. on_delete
40. limit_choices_to
41. related_name
42. related_query_name
43. db_constraint
44. swappable
45. symmetrical
46. through
47. through_fields
48. db_table
49. parent_link
50. db_default

1. null - определяет значение NULL в DB.
2. blank - определяет пустое поле в форме.

3. choices # Принимает сопоставления или вызываемый обьект для выбора.

Пример:

SPORT_CHOICES = {
    "Martial Arts": {"judo": "Judo", "karate": "Karate"},
    "Racket": {"badminton": "Badminton", "tennis": "Tennis"},
    "unknown": "Unknown",
}

def get_scores():
    return [(i, str(i)) for i in range(10)]

class Winner(models.Model):
    sport = models.CharField(choices=SPORT_CHOICES)
    score = models.IntegerField(choices=get_scores) 

4. db_column - принимает строку с именем столбца для DB.
5. db_comment - принимает строку с комментарием к полю в DB.
6. db_index - создает индекс для поля в DB для ускорения поиска. (TODO)
7. db_tablespace - принимает строку с именем пространства имен DB для хранения данных. (TODO)
8. default - принимает значение по умолчанию для поля.
9. editable - определяет редактируемость поля.
10. error_messages - словарь сообщений об ошибках поля.
11. help_text - принимает строку с пояснительным текстом для поля.
12. primary_key - делает поле первичным ключом.
13. unique - гарантирует уникальность поля в модели.
14. unique_for_date, unique_for_month, unique_for_year - принимает имя поля даты уникального значения.
15. verbose_name - принимает строку человекочитаемого имя для поля в admin panel.
16. validators - принимает список пользовательских валидаторов для проверки значения поля.
17. auto_now - автоматическое присваивание текущей даты/времени при сохранении обьекта.
18. auto_now_add - автоматическое присваивание текущей даты/времени при создании обьекта.
19. max_length - максимальная длина строкового поля.
20. min_length - минимальна длина строкового поля.
21. db_collation - имя сопоставления DB для поля.
22. max_digits - максимально допустимое кол-во цифр для хранения чисел с плавающей точкой.
23. decimal_places - кол-во десятичных знаков для хранения чисел с плавающей точкой.
24. upload_to - относительный путь или функция для загрузки файлов.
25. storage - обьект хранения на кастомное хранилище для файла.
26. path - абсолютный путь файловой системы к каталогу для выбора.
27. match - регулярное выражение в виде строки для валидации имен файлов.
28. recursive - включение подкаталогов.
29. allow_files - включение файлов в указанном расположении.
30. allow_folders - включение папок в указанном расположении.
31. protocol - строка, ограничивающая допуск входных данных указанным протоколом (both, IPv4, IPv6).
32. unpack_ipv4 - распаковка адресов IPv4.
33. height_field - имя поля модели, содержащее высоту изображения.
34. width_field - имя поля модели, содержащее ширину изображения.
35. encoder - подкласс для сериализации значения из DB.
36. decoder - подкласс для десериалазции значения, полученного из DB.
37. allow_unicode - принятие букв Unicode в дополнение к буквам ASCII.
38. to_field - строка с именем модели или класс модели, с которой устанавливается отношение.
39. on_delete - ограничение при удалении связанного обьекта (CASCADE: удаляет все обьекты, которые ссылаются на удаляемый обьект; PROTECT: предотвращает удаление связанного обьекта; SET_NULL: устанавлиевает значение NULL; SET_DEFAUL: устанавливает значение по умолчанию; SET(): устанавливает указанное значение; DO_NOTHING: ничего не делает; RESTRICT: предотвращает удаление связанного обьекта).
40. limit_choices_to - ограничение на доступный выбор.
41. related_name - имя для связи от связанного обьекта обратно к этому обьекту.
42. related_query_name - имя которое будет использоваться в качестве имени обратного фильтра из целевой модели.
43. db_constraint - ограничение в DB для этого внешнего ключа. По умолчанию True.
44. swappable - управление реакцией среды миграции. По умолчанию True.
45. symmetrical - используется только в определении ManyToManyField для себя 'self'.
46. through - промежуточная таблица для управления отношениями многие ко многим.
47. through_fields - определение полей промежуточной модели. Используется после through.
48. db_table - имя таблицы для хранения данных типа многие ко многим.
49. parent_link - следует ли поле использовать в качестве ссылки на родительский класс, а не как доп. поле.

50. db_default # Значение по умолчанию, вычисленное БД.

Пример:

class MyModel(models.Model):
    age = models.IntegerField(db_default=18)
    created = models.DateTimeField(db_default=Now())
    circumference = models.FloatField(db_default=2 * Pi())
"""



"""
# Model Meta options (Мета опции моделей)

1. abstract
2. app_label
3. base_manager_name
4. db_table
5. db_table_comment
6. db_tablespace
7. default_manager_name
8. default_related_name
9. get_latest_by
10. managed
11. order_with_respect_to
12. orderding
13. permissions
14. default_permissions
15. proxy
16. required_db_features
17. required_db_vendor
18. select_on_save
19. indexes
20. unique_together
21. index_together
22. contraints
23. verbose_name
24. verbose_name_plural
25. label
26. label_lower

1. abstract - сделать модель абстрактным базовым классом. Не создает таблицу в DB.
2. app_label - имя приложения к которому принадлежит.
3. base_manager_name - имя атрибута менеджера. По умолчанию objects.
4. db_table - имя таблицы DB для расширения родительского мета-класса.
5. db_table_comment - комментарий к таблице DB.
6. db_tablespace - имя табличного пространства DB.
7. default_manager_name - имя менеджера для модели.
8. default_related_name - имя для связи от связанного обьекта к этому обьекту. По умолчанию <model_name>_set/
9. get_latest_by - имя поля или список полей для методов latest(), earliest().
10. managed - Создание таблицы DB во время миграции. По умолчанию True.
11. order_with_respect_to - упорядочивание связанных обьектов относительно родительского класса.
12. orderding - порядок при получении обьектов.
13. permissions - список доп. разрешений для ввода в таблицу разрешений при создании обьекта.
14. default_permissions - список разрешений для модели.
15. proxy - модель, которая является подклассом другой модели.
16. required_db_features - список функций DB, которое должно иметь текущее соединение, чтобы модель учитывалась на этапе миграции.
17. required_db_vendor - имя поддерживаемого поставщика DB, для которого предназначена модель.
18. select_on_save - использование алгоритма версии до 1.6 save(). По умолчанию False.
19. indexes - список индексов в модели.
20. unique_together - список имен полей, которые должны быть уникальными.
21. index_together - список имен полей, которые вместе индексируются. Устарело.
22. contraints - список ограничений в модели.
23. verbose_name - удобочитаемое имя обьекта в един. числе. По умолчанию имя класса.
24. verbose_name_plural - имя обьекта во множ. числе. По умолчанию verbose_name + 's'.
25. label - представление обьекта, возвращает app_label.object_name.
26. label_lower - представление модели, возвращает app_label.model_name.
"""



"""
# Model field attribute (Атрибуты полей моделей)

1. Field.auto_created - было ли поле создано автоматически.
2. Field.concrete - имеет ли поле связанный с ним столбец DB.
3. Field.hidden - используется ли поле для другого нескрытого поля.
4. Field.is_relation - содержит ли поле ссылки на другие модели.
5. Field.model - модель в которой определено поле.
6. Field.many_to_many - имеет ли поле отношение многие ко многим.
7. Field.many_to_one - имеет ли поле отношение многие к одному.
8. Field.one_to_many - имеет ли поле отношение один ко многим.
9. Field.one_to_one - имеет ли поле отношение один к одному.
10. Field.related_model - модель к которой относится поле.
"""



"""
# Related objects reference

1. add
2. create
3. remove
4. clear
5. set

1. add(*objs, bulk=True, through_defaults=None) - добавляет обьекты в набор обьектов.
2. create(through_defaults=None) - создает новый обьект и добавляет его в набор обьектов.
3. remove(*objs, bulk=True) - удаляет указанный обьект.
4. clear(bulk=True) - удаляет все обьекты.
5. set(objs, bulk=True, clear=False, through_defaults=None) - замена набора обьектов.
"""


"""
# Model instance reference (Управление моделями)

product.name = 'name'
product.save(update_fields['name'])
Если в передан список имен полей, то будут обновлены только они и это повысит производительность.

Model.from_db(db, field_names, values) - метод для настройки создания экземпляра модели при загрузке из DB. (db: псевдоним DB модели; field_names: имена всех загруженных полей; values: загруженные значения для каждого поля в field_names)
Model.refresh_from_db(using=None, fields=None) - перезагрузка значений модели из DB. (using: принудительная перезагрузка DB; fiels: принудительная загрузка набора полей)
Model.get_deferred_fields() - вспомогательный метод, возвращающий имена атрибутов всех полей, которые отложены в модели.
Model.clean_fields(exclude) - проверяет все поля модели (exclude: имена полей для исключения из проверки).
Model.clean() - проверка модели, изменение атрибутов модели. Переопределяемый метод. Чтобы назначить исключение определенному полю, необходимо создать словарь ValidationError, где ключи это имена полей.
Model.validate_unique(exclude=None) - аналогичен clean_fields(), но проверяет ограничения уникальности unique, unique_for_date, unique_for_month, unique_for_year, unique_together.
Model.validate_constraints(exclude=None) - проверяет все ограничения определенные в Meta.constraints.
Model.full_clean(exclude=None, validate_unique=True, validate_constraints=True) - вызывает clean_fields(), clean(), validate_unique(), validate_constraints().
Model.save(force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None) - сохранение экземпляра (update_fields: список имен полей для обновления, повышает производительность).
Model.delete(using=DEFAULT_DB_ALIAS, keep_parents=False) - удаление обьектов
Model.__str__() - удобочитаемое предстваление модели.
Model.__eq__().
Model.__hash__() - основан на значении первичного ключа экземпляра.
Model.get_absolute_url() - строка, содержащая ссылку на обьект. Рекомендуется использовать reverse().
Model.get_FOO_display() - возвращает читабельное значение поля (FOO это имя поля у choices обьекта).
Model.get_next_by_FOO(**kwargs):
Model.get_previous_by_FOO(**kwargs) - возвращает следующий и предыдущий обьект относительно поля даты (FOO - имя поля).
Model._state - отслеживание статуса экземпляра модели. Имеет два атрибута adding и db. adding=True - модель не сохранена в DB, db - строка псевдонима DB из которой был получен экземпляр.
"""


"""
## QuerySet (Создание запросов)
QuerySet - ленивый запрос, не требующий каких-либо действий с DB. Запрос в DB только после обращения в QuerySet.



### Методы менеджеров

all() - возвращает QuerySet, содержащий все обьекты.
get(*args, **kwargs) - возвращает обьект, содержащий один элемент по запросу. Если нет результатов или более одного, то будет исключение.
create(**kwargs) - создает и сохраняет обьект.
get_or_create(default=None, **kwargs) - поиск обьекта по значениям, если нет, то создает его. Возвращает кортеж, где [0] - обьект, [1] - был ли создан обьект.
update_or_create(default=None, **kwargs) - обновление обьекта по значениям, если нет, то создает его. Возвращает кортеж, где [0] - обьект, [1] - был ли создан обьект.
filter(*args, **kwargs) - возвращает QuerySet, содержащий обьекты, которые соответствуют заданным параметрам поиска.
filter(*args, **kwargs)[:5] - возвращает QuerySet, содержащий первые 5 обьектов.
filter(*args, **kwargs)[0] - возвращает QuerySet, содержащий один элемент по запросу.
exclude(*args, **kwargs) - возвращает QuerySet, содержащий обьекты, которые не соответствуют заданным параметрам поиска.
order_by(*fields) - принимает имена полей для сортировки QuerySet. Для рандома - "?".
annotate(*args, **kwargs) - генерация агрегатов для каждого элемента в QuerySet. Позволяет добавить в каждый обьект в QuerySet дополнительные данные.
alias(*args, **kwargs) - то же что и annotate, но вместо добавления данных, создает временую переменную с данными для послед. использования с другими методами.
reverse() - переворачивает порядок элементов.
distinct(*fields) - исключает повторяющиеся обьекты и возвращает новый QuerySet.
values(*fields, **expressions) - возвращает QuerySet, который возвращает словари, а не экземпляры модели.
values_list(*fields, flat=False, named=False) - похоже на values(), но возвращает кортежи. (flat: True, если передается одно поле; named: получить результаты как namedtuple()).
dates(field, kind, order='ASC') - возвращает QuerySet, который представляет список datetime.date обьектов (field: название поля DateField; kind: (year, month, week, day); order: упорядочивание резултатов (ASC, DESC)).
datetimes(field_name, kind, order='ASC', tzinfo=None, is_dst=None) - возвращает QuerySet, который представляет список datetime.datetime (field_name: название поля DateTimeField; kind: то же, что и dates(); order: то же, что и dates(); tzinfo: часовой пояс).
none() - возвращает пустой QuerySet.
union(*other_qs, all=False) - обьединяет несколько QuerySet (all: разрешить повторяющиеся значения).
intersection(*other_qs) - возвращает общие элементы нескольких QuerySet.
difference(*other_qs) - сохраняет элементы в QuerySet.
select_related(*field) - возвращает QuerySet, дополняя данные обьекта. Повышает производительность, уменьшая кол-во запросов к DB. В итоге один запрос.
prefetch_related(*lookups) - возвращает QuerySet, который автоматически извлекает связанные обьекты для указанных lookups. В итоге два запроса.
extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None) - позволяет вставить свой SQL запрос (select: добавить в SELECT предложение доп. поля; where/tables: опреденить WHERE преложения; ...). Не рекомендуется к использованию. Не безопасен, так как способствует SQL-иньекции.
defer(*fields) - принимает список полей для отложенного набора, которые обрабатываются только при вызове. Полезно для больших данных.
only(*fields) - противоположен defer(). перечисленные поля загружаются немедленно.
using('alias') - выбор вызываемой DB, если используется несколько (alias: имя DB из DATABASES)).
select_for_update(nowait=False, skip_locked=False, of=(), no_key=False) - возвращает набор запросов, который будет блокировать строки DB до конца транзакции. Полезно, когда необходимо гарантировать неизменность строк другими транзакциями.
raw(raw_query, params=(), translations=None, using=None) - берет необработанный SQL-запрос и возвращает RawQuerySet.
bulk_create(objs, batch_size=None, ignore_conflicts=False, update_conflicts=False, update_fields=None, unique_fields=None) - эффективное добавление списка обьектов DB одним запросом. Возвращает созданные обьекты списком (batch_size: сколько обьектов создается в одном запросе; ignore_conflicts: игнор. ошибок; update_conflicts: обновлять ли поля, если вставка строки не удалась.).
bulk_update(objs, fields, batch_size=None) - эффективно обновляет поля одним запросом. Возвращает кол-во обновленных обьектов.
count() - возвращает количество обьектов в DB по QuerySet.
in_bulk(id_list=None, *, field_name='pk') - принимает список значений полей и field_name для этих полей и возвращает словарь, сопоставляющий каждое значение с экз. обьекта с задан. значением поля.
iterator(chunk_size=None) - оценивает QuerySet и возвращает итератор.
latest(*fields) - возвращает последний обьект в таблице по заданным полям.
earliest(*fields) - наоборот latest().
first() - возвращает первый обьект, соответ. набору запросов.
last() - наоборот first().
aggregate(*args, **kwargs) - позволяет выполнить вычисления данными DB. Возвращает результат работы агрегатного запроса.
exists() - есть ли результаты в QuerySet.
contains(obj) - содержит ли QuerySet obj.
update(**kwargs) - выполняет запрос обновления SQL для указанных полей и возвращает кол-во строк. Выполняется моментально.
delete() - Выполняет SQL-запрос на удаление для всех строк в QuerySet и возвращает количество удаленных объектов, а также словарь с количеством удалений для каждого типа объекта.
as_manager() - возвращает экземпляр Manager с копией QuerySet.
explain(format=None, **options) - возвращает подробную информацию о том, как БД выполняет запрос, включая индексы и соединения. Используется для оценки запроса для оптимизации.



### Field lookups (Поиск по полям)

1. exact - полное совпадение.
2. iexact - полное совпадение без учета регистра.
3. contains - совпадение с учетом регистра.
4. icontains - совпадение без учета регистра.
5. startswith - начинается с.
6. endswith - заканчивается на.
7. istartswith - начинается с без учета регистра.
8. iendswith - заканчивается на без учета регистра.
9. isnull - пустое ли поле.
10. in - внутри массива.
11. gt - больше.
12. gte - больше или равно.
13. lt - меньше.
14. lte - меньше или равно.
15. range - в промежутке.
16. date - дата.
17. year - год.
18. iso_year - год ISO 8601.
19. month - месяц.
20. day - день.
21. week - номер недели.
22. week_day - день недели.
23. iso_week_day - день недели USO-8601.
24. quarter - квартал года.
25. time - время.
26. hour - час.
27. minute - минута.
28. second - секунда.
29. regex - регулярное выражение.
30. iregex - регулярное выражение без учета регистра.



### Aggregation functions (Функции агрегирования)
- django.db.models

expressions - строки, ссылающиеся на поля модели.
output_field - поле модели возвращаемого значения.
filter - параметр фильтрации агрегируемых строк.
default - значение по умолчанию.
**extra - аргументы ключевых слов доп. контекта для SQL.

1. F(query) - обьект ссылающийся на значения поля модели без извлечения из DB. Предназначен для сравнения значений полей одной модели.
```python
reporter = Reporters.objects.get(name='John')
reporter.stories_filed += 1
reporter.save()
# Заменяем на
Reporter.objects.filter(name='John').update(stories_filed=F('stories_filed') + 1)
```
2. Min(expression, output_field=None, filter=None, default=None, **extra) - возвращает минимальное значение данного выражения.
3. Max(expression, output_field=None, filter=None, default=None, **extra) - возвращает макс. значение данного выражения.
4. StdDev(expression, output_field=None, sample=False, filter=None, default=None, **extra) - 
5. Outer()
6. Count(expression, distinct=False, filter=None, **extra) - возвращает кол-во обьектов по указанному выражению.
7. Subquery(field) - добавление явного подзапроса к QuerySet.
8. Sum(expression, output_field=None, sample=False, filter=None, default=None, **extra) - вычисляет сумму всех значений данного выражения.
9. Q(query) - обьект используемый для инкапсуляции набора запросов. Пример: Q(name='name'). Можно комбинировать с помощью операторов & (И), | (ИЛИ) и ^ (Исключающее ИЛИ). Запрос можно конвертировать: ~ (НЕ).
10. Prefetch(search, queryset=None, to_attr=None) - обьект для управления работой prefetch_related().
11. Variance(expression, output_field=None, sample=False, filter=None, default=None, **extra) - возвращает дисперсию данных в предоставленном выражении.
12. StdDev(expression, output_field=None, sample=False, filter=None, default=None, **extra) - возвращает стандартное отклонение данных в представленном выражении.
13. Func(*expressions, **extra) - базовый тип всех выражений.
14. Aggregate() - агрегатное выражение.
15. Value() - обьект представляющий простое значение. Редко используется явно.
16. ExpressionWrapper() - окружает другое выражение и обеспечивает доступ к св-м.
17. Exists(queryset) - подкласс Subquery, использующий EXISTS оператор SQL.
18. When(condition=None, then=None, **lookups) - обьект для инкапсуляции условия и его результата для использования в выражении.
19. Case(*cases, **extra) - выражение похоже на if, elif, else. Каждый condition оценивается по порядку пока не будет получено истинное значение.
20. Avg(expression, output_field=None, distinct=False, filter=None, default=None, **extra) - возвращает среднее значение заданного числового выражения.
"""


"""
class Manager
 - интерфейс, предоставляющий запросы к DB моделям Django. У каждой модели есть хотя бы один Manager.

Выполнение необработанных запросов. Написание чистого SQL.

Manager.raw(raw_query, params=(), translations=None).
Person.objects.raw("SELECT * FROM myapp_person") == Person.objects.all().
Ожидается что будет возвращен набор строк DB, никаких проверок нет.

Способы:
1.
name_map = {'first': 'first_name', 'last': 'last_name', 'pk': 'id'}
Person.objects.raw("SELECT * FROM some_other_table", translations=name_map)
2.
lname = 'Doe'
Person.objects.raw("SELECT * FROM myapp_person WHERE last_name = %s", [lname])

Выполнение пользовательского SQL.
- django.db.connection

connection.cursor() - получение обьекта курсора.
cursor.execute(sql, [params]), cursor.fetchone(), cursor.fetchall().
```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [baz])
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [baz])
    row = cursor.fetchone()
```

Чтобы защититься от SQL-иньекций, не нужно заключать в кавычки заполнители %s.
"""


"""
Транзакции DB.


Прежде чем вызвать функцию просмотра, запускается транзакция. Если ответ получен, то транзакция фиксируется, если нет, то удаляется.
Если ATOMIC_REQUESTS включен, то чтобы выключить транзакцию для представления используют non_atomic_requests декоратор.

Управление транзакциями
1. atomic(using=None, savepoint=True, durable=False) - (using: имя DB; savepoint: управление точками сохранения; durable:).
```python
from django.db import transaction
@transaction.atomic
def viewfunc(request):
    pass
```
ИЛИ
```python
with transaction.atomic():
    pass
```
ИЛИ
```python
try:
    with transaction.atomic():
        pass
except:
    pass
```

2. on_commit(func, using=None, robust=False) - вызываемые методы после успешной фиксации транзакции (robust: выполнение обратных вызовов).

"""


"""
# Список SQL запросов

Доступно только при DEBUG=True

from django.db import connection, reset_queries

connection.queries - получить список запросов
connection.queries.clear() - очистить список запросов
reset_queries() - очиситить список запросов
"""


"""
Разработка проекта

Рекомендуется использовать django-debug-toolbar для контроля DB.
"""


"""
Database access optimization (Оптимизация доступа к БД).

Методы оптимизации:
1. Использование индексов. Индексы к частозапрашиваемым полям ускоряют поиск по БД.
2. Понимание QuerySet. Важно понимать как работает QuerySet для хорошей производительности.
3. Использование filters, F(), annotate.
4. Использование RawSQL.
5. Использование чистого SQL.
6. select_related(), prefetch_related() - получение всех данных за один запрос.
7. values(), values_list() - если нужны только словарь или список значений и не нужны модели ORM.
8. defer(), only() - управление столбцами БД, которые точно не понадобятся.
9. count() != len(queryset) - только подсчет, а не выполнение. Не злоупотреблять.
10. update(), delete() - массовое удаление и обновление выгодней не массовой.
11. entry.blog_id != entry.blog.id - если нужно получить только внешний ключ.
12. bulk_create() - массовое создание обьектов выгодно поочередного.
13. bulk_update() - массовое обновление обьектов выгодней поочередного.
14. add() - массовая вставка ManyToManyField уменьшает кол-во запросов.
15. remove() - массовое удаление обьектов ManyToManyField выгоднее одиночного.
"""


"""
Контроллирование запросов.

def blocker(execute, sql, params, many, context):
    raise Exception('No database access allowed here')
ИЛИ
class QueryLogger:
    def __init__(self):
        self.queries = []
    
    def __call__(self, execute, sql, params, many, context):
        current_query = {"sql": sql, "params": params, "many": many}
        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            current_query["status"] = "error"
            current_query["exception"] = e
            raise
        else:
            current_query["status"] = "ok"
            return result
        finally:
            duration = time.monotonic() - start
            current_query["duration"] = duration
            self.queries.append(current_query)
    
def my_view(request):
    with connection.execute_wrapper(blocker):
        return render(request, template_name, context)
"""


"""
ManyToMany relationships (Отношения многие ко многим). Пример


>>> from django_manual.models import Publication, Article
>>> p1 = Publication(title='pub1')
>>> p2 = Publication(title='pub2')
>>> p3 = Publication(title='pub3')
>>> Publication.objects.bulk_create([p1,p2,p3])
[<Publication: pub1>, <Publication: pub2>, <Publication: pub3>]
>>> Article(headline='headline1')
<Article: headline1>
>>> Article(headline='headline1').save()
>>> a1 = Article.objects.get(headline='headline1')
>>> a1.publications.add(p1,p2)
>>> a2 = Article(headline='headline2')
>>> a2.save()
>>> a2.publications.add(p2,p3)
>>> p4 = a2.publications.create(title='pub4')
>>> a2.publications.all()
<QuerySet [<Publication: pub2>, <Publication: pub3>, <Publication: pub4>]>
>>> p2.article_set.all()
<QuerySet [<Article: headline1>, <Article: headline2>]>
>>> Article.objects.filter(publications__id=1)
<QuerySet [<Article: headline1>]>
>>> Article.objects.filter(publications__title__startswith='pub')
<QuerySet [<Article: headline1>, <Article: headline1>, <Article: headline2>, <Article: headline2>, <Article: headline2>]>
>>> Article.objects.filter(publications__title__startswith='pub').distinct()
<QuerySet [<Article: headline1>, <Article: headline2>]>
>>> Article.objects.filter(publications__title__startswith='pub').count()
5
>>> Article.objects.filter(publications__title__startswith='pub').distinct().count()
2
>>> Article.objects.exclude(publications=p1)
<QuerySet [<Article: headline2>]>
>>> p1.delete()
(2, {'django_manual.Article_publications': 1, 'django_manual.Publication': 1})
>>> a2.delete()
(4, {'django_manual.Article_publications': 3, 'django_manual.Article': 1})
>>> p2.article_set.all()
<QuerySet [<Article: headline1>]>
>>> p2.article_set.remove(a1)
"""

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title
    

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self) -> str:
        return self.headline


"""
ManyToOne relationships (Отношения многие к одному). Пример


>>> r = Reporter(first_name='John', last_name='Smith', email='john@example.com')
>>> r.save()
>>> r2 = Reporter(first_name='Paul', last_name='Jones', email='paul@example.com')
>>> r2.save()
>>> a = Article2(id=None, headline='headline1', pub_date=date(2005, 7, 27), reporter=r)
>>> a.save()
>>> a.reporter_id
1
>>> a.reporter
<Reporter: John Smith>
>>> a2 = Article2.objects.create(headline='headline2', pub_date=date(2000, 10, 10), reporter=r2)
>>> a2
<Article2: headline2>
>>> a3 = r.article2_set.create(headline='headline3', pub_date=date(2001, 11, 11))
>>> r.article2_set.all()
<QuerySet [<Article2: headline1>, <Article2: headline3>]>
>>> r.article2_set.count()
2

"""

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
    

class Article2(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.headline
    
    class Meta:
        ordering = ['headline']


"""
OneToOne relationships (отношения один к одному). Примеры.


>>> p1 = Place(name='place1', address='address1')
>>> p1.save()
>>> p2 = Place(name='place2', address='address2')
>>> p2.save()
>>> r = Restaurant(place=p1)
>>> r.save()
>>> p1.restaurant
<Restaurant: place1>
>>> r.place
<Place: place1>
>>> w = r.waiter_set.create(name='w1')
"""


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name
    

class Restaurant(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    
