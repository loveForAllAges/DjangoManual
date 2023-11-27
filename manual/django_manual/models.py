from django.db import models


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


"""
# Example

>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles, date_joined=date(1962, 8, 16), invite_reason="Needed a new drummed.")
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> beatles.members.add(paul, through_defaults={'date_joined': date(1960, 8, 1)})
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
>>> beatles.members.clear()
>>> beatles.members.all()
<QuerySet []>
>>> beatles.members.create(name="George Harrison", through_defaults={'date_joined': date(1960, 8, 1)})
<Person: George Harrison>
>>> beatles.members.all()
<QuerySet [<Person: George Harrison>]>
>>> beatles.members.set([ringo, paul], through_defaults={'date_joined': date(1960, 8, 1)})
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> Group.objects.filter(members__name__startswith="Paul")
<QuerySet [<Group: The Beatles>]>
>>> Person.objects.filter(group__name="The Beatles", membership__date_joined__gt=date(1960, 1, 1))
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
"""


"""
# Model field types

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
"""



"""
# Model field options

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
11. help_textyf
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

1. null - определяет значение NULL в DB.
2. blank - определяет пустое поле в форме.
3. choices - принимает список кортежей, чтобы задать список допустимых значений для поля.
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
"""



"""
# Model Meta options

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
# Model field attribute

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
annotate(*args, **kwargs) - позволяет добавить в каждый обьект в QuerySet дополнительные данные.
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
using(alias) - контроль вызываемой DB, если используется несколько (alias: имя DB из DATABASES)).
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
aggregate(*args, **kwargs) - возвращает словарь значений с доп. данными.
exists() - есть ли результаты в QuerySet.
contains(obj) - содержит ли QuerySet obj.
update(**kwargs) - выполняет запрос обновления SQL для указанных полей и возвращает кол-во строк. Выполняется моментально.
delete() - Выполняет SQL-запрос на удаление для всех строк в QuerySet и возвращает количество удаленных объектов, а также словарь с количеством удалений для каждого типа объекта.
as_manager() - возвращает экземпляр Manager с копией QuerySet.
explain(format=None, **options) - возвращает строку QuerySet с планом выполнения запроса.



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
"""
