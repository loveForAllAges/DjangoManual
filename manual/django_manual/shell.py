'''
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



>>> from django_manual.models import Book, Author, Publisher, Store
# Кол-во книг
>>> Book.objects.count()
# Кол-во книг с автором AA
>>> Book.objects.filter(publisher__name="AA").count()
# Средняя цена всех книг
>>> Book.objects.aggregate(Avg("price", default=0))
{'price__avg': Decimal('0')}
# Макс. цена всех книг
>>> Book.objects.aggregate(Max("price", default=0))
{'price__max': Decimal('90')}
# Разница максимальной цены и средней
>>> Book.objects.aggregate(price_diff=Max("price") - Avg("price"))
{'price_diff': Decimal('44')}
# Кол-во книг первого публициста
>>> Publisher.objects.annotate(num_books=Count('book'))[0].num_books
0
# Кол-во книг публициста с рейтингом больше 5 и меньше 5
>>> a = Count('book', filter=Q(book__rating__gt=5))
>>> b = Count('book', filter=Q(book__rating__lte=5))
>>> p = Publisher.objects.annotate(b=b).annotate(a=a)
>>> p.first().a
0
>>> p.first().b
0
# Топ 5 публицистов по убыванию
>>> p = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
>>> p.first().num_books
10
# Получение средней цены всех книг:
>>> Book.objects.all().aggregate(Avg('price'))
# Или:
>>> Book.objects.aggregate(Avg('price'))
# Сгенерировать несколько агрегатов:
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': Decimal('46'), 'price__max': Decimal('90'), 'price__min': Decimal('10')}
# Создать агрегат для каждого элемента:
>>> q = Book.objects.annotate(num_authors=Count('authors'))
>>> q[0].num_authors
0
>>> q[1].num_authors
2
# Нельзя обьединять несколько агрегатов: Book.objects.annotate(Count('authors'), Count('store')).
# Но у Count есть параметр distinct который это разрешает:
>>> q = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
# Узнать диапазон цен каждого магазина:
<QuerySet [<Store: Store object (1)>, <Store: Store object (2)>]>
>>> ss = Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
>>> ss[0].max_price
Decimal('20')
>>> ss[0].min_price
Decimal('10')


# Массовое создание обьектов выгоднее поочередного
>>> p1 = Person(name='Test person 1')
>>> p2 = Person(name='Test person 2')
>>> Person.objects.bulk_create([p1,p2])
[<Person: Test person 1>, <Person: Test person 2>]

# Массовое обновлние обьектов выгоднее поочередного
>>> p3 = Person(name='Test person 3')
>>> p4 = Person(name='Test person 4')
>>> pc = Person.objects.bulk_create([p3,p4])
>>> pc[0].name = 'upd name 3'
>>> pc[1].name = 'upd name 4'
>>> Person.objects.bulk_update(pc, ['name'])
2
'''