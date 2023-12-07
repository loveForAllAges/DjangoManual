"""
Раздел: Pagination (Пагинация)


Paginator - родительский класс пагинаторов.

Пример:
>>> from django.core.paginator import Paginator
>>> p = list(Person.objects.all())
>>> obj = list(Person.objects.all())
>>> p = Paginator(obj, 2)
>>> p.count
7
>>> p.num_pages
4
>>> p.page_range
range(1, 5)
>>> p1 = p.page(1)
>>> p1
<Page 1 of 4>
>>> p1.object_list
[<Person: Ringo Starr>, <Person: Paul McCartney>]
>>> p2 = p.page(2)
>>> p2.object_list
[<Person: George Harrison>, <Person: Test person 1>]
>>> p2.has_next()
True
>>> p2.has_previous()
True
>>> p2.has_other_pages()
True
>>> p2.next_page_number()
3
>>> p2.previous_page_number()
1
>>> p2.start_index()
3
>>> p2.end_index()
4



Разбивка на страницы ListView:

from django.views.generic import ListView
from myapp.models import Contact


class ContactListView(ListView):
    paginate_by = 2
    model = Contact


{% for contact in page_obj %}
    {# Each "contact" is a Contact model object. #}
    {{ contact.full_name|upper }}<br>
    ...
{% endfor %}

<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>



В функции:
from django.core.paginator import Paginator
from django.shortcuts import render
from myapp.models import Contact


def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "list.html", {"page_obj": page_obj})
"""