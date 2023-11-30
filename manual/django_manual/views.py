from typing import Any
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from datetime import date

from .models import Author, Book

"""
Decorators (Декораторы)
django.views.decorators


1. require_http_methods(request_method_list)
Декоратор пропускает методы из списка.
2. require_GET()
Декоратор пропускает метод GET.
3. require_POST()
Декоратор пропускает метод POST.
4. require_safe()
Декоратор пропускает методы GET и HEAD.
5. condition(etag_func=None, last_modified_func=None)
6. etag(etag_func)
7. last_modiftied(last_modified_func)
Декоратор для создания заголовков ETag и Last-Modified.
8. gzip_page()
Декоратор сжатия контента для каждого просмотра. Устанавливает Vary заголовок так, что кеши будут основывать свое хранилище на Accept-Encoding заголовке.
9. vary_on_cookie(func)
10. vary_on_headers(*headers)
Декоратор для управления кешированием. Заголовок Vary опр. какие заголовки запросов механиз кеширования должен учитывать при построении своего ключа кеша.
11. cache_control(**kwargs)
Декоратор исправляет заголовок Cache-Control, добавляя все аргументы ключевого слова.
12. never_cache(view_func)
Декоратор добавляет заголовки, если их нет: Expires к текущей дате/времени; Cache-Control: max-age=0, no-cache, no-store, must-revalidate, private страница никогда не будет кешироваться.
13. no_append_slash()
Декоратор позволяет исключить отдельные представления из APPEND_SLASH нормализации URL-адресов.
"""

"""
File uploads (Загрузка файлов)


Загруженные файлы помещаются в request.FILES в виде словаря.
HTML форма должна иметь атрибут enctype="multipart/form-data".

До сохранения Django хранит загруженные файлы в памяти, если размер меньше 2.5 МБ. Иначе загруженный файл будет будет записан во временный файл во временном каталоге.


Изменение обработчиков загрузки на лету
Например для обратной связи о ходе загрузки в ajax.
Необходимо переопределить request.upload_handlers.
"""


class UploadFileForm(forms.Form):
    file = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse('Успешно')
        else:
            return HttpResponse('Провал')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


# Загрузка нескольких файлов одним полем формы

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()


class FileFieldFormView(generic.FormView):
    form_class = FileFieldForm
    template_name = 'upload_file.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        for f in files:
            print('File - ', f)
        return super().form_valid(form)



"""
Shortcut functions (Функции быстрого доступа)
django.shortcuts


1. render(request, template_name, context=None, content_type=None, status=None, using=None)
Обьединяет заданный шаблон с контекстом и возвращает HttpResponse.
Аргументы: request - обьект запроса; template_name - полное имя используемого шаблона; context - словарь доп. значений; content_type - тип MIME; status - код состояния ответа; using - механизм шаблонов.

2. redirect(to, *args, permanent=False, **kwargs)
Возвращает HttpResponseRedirect URL-адрес для переданных аргументов.
Аргументы: permanent - временное или постоянное перенаправление; абсолютный или относительный url или имя представления.

3. get_object_or_404(klass, *args, **kwargs)
Вызывает get() менеджера модели.

4. get_list_or_404(klass, *args, **kwargs)
Возвращает результат приведения данного менеджера моделей к списку (klass: обьект Model; *args: Q обьекты; **kwargs: параметры поиска в формате как get() или filter()).
"""

"""
Class-based views API (Представления на основе классов)


1. View
2. TemplateView
3. RedirectView
4. DetailView
5. ListView
6. FormView
7. CreateView
8. UpdateView
9. DeleteView
10. ArchiveIndexView
11. YearArchiveView
12. MonthArchiveView
13. WeekArchiveView
14. DayArchiveView
15. TodayArchiveView
16. DateDetailView
"""

"""
1. View

Базовый класс представления. Все остальные наследуются от него.

Атрибуты:
    - http_method_names - список методов HTTP, которые принимает представление.
    По умолчанию: ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
Методы:
    - as_view(**initkwargs) - возвращает вызываемое представление, которое принимает запрос и возвращает ответ.
    - setup(request, *args, **kwargs) - выполняет инициализацию ключевого представления до dispatch(). При переопределении обязателен super().
    - dispatch(request, *args, **kwargs) - метод, который принимает request и аргументы и возвращает HTTP-ответ. Проверяет метод HTTP и делегирует методу, соответствующему методу HTTP (get, post, ...).
    - options(request, *args, **kwargs) - обрабатывает ответ на запросы HTTP-команды OPTIONS. Возвращает ответ с Allow заголовком, содержащим список разрешенных имен HTTP-методов представления.
    - http_method_not_allowed(request, *args, **kwargs) - возвращает HttpResponseNotAllowed и список разрешенных методов виде обычного текста. Вызывается если представление не поддерживает метод HTTP.
"""

class CustomView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('View page')


"""
2. TemplateView

Отображает заданный шаблон с контекстом, содержащим параметры, зафиксированные в URL-адресе.
"""

class CustomTemplateView(generic.TemplateView):
    template_name = 'view.html'


"""
3. RedirectView

Перенаправляет на заданный URL.
"""

class CustomRedirectView(generic.RedirectView):
    # Должно ли перенаправление быть постоянным (301 или 302 код состояния).
    permanent = False
    # Передавать ли строку запроса GET в новое место.
    query_string = True
    # Имя шаблона URL-адреса для перенаправления.
    pattern_name = 'class-view'

    # Создает целевой URL-адрес для перенаправления.
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        # ...
        return super().get_redirect_url(*args, **kwargs)
    

"""
4. DetailView

Содержит обьект (self.object) над которым работает представление.
"""

class CustomDetailView(generic.DetailView):
    model = Author
    template_name = 'object.html'


"""
5. ListView

Содержит список обьектов (self.object_list) над которыми работает представление.
"""

class CustomListView(generic.ListView):
    template_name = 'object-list.html'
    model = Author


"""
6. FormView

Представление, отображающее форму. В случае ошибки повторно отображает форму с ошибками проверки, в случае успеха перенаправляет на новый URL.
"""

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        pass


class CustomFormView(generic.FormView):
    template_name = 'form-view.html'
    form_class = ContactForm
    success_url = '/views/View'

    def form_valid(self, form: Any) -> HttpResponse:
        form.send_email()
        return super().form_valid(form)


"""
7. CreateView

Представление, отображающее форму для создания обьекта, повторное отображение формы с ошибками проверки и сохранение обьекта.

Атрибуты:
    - template_name_suffix - суффикс шаблона.
    - object - есть доступ к создаваемому обьекту (self.object). Если обьект еще не создан - None.
Методы:
    - get(request, *args, **kwargs)
    - post(request, *args, **kwargs)
"""

class CustomCreateView(generic.CreateView):
    model = Author
    fields = '__all__'
    success_url = '/views/View'
    template_name = 'create-view.html'


"""
8. UpdateView

Представление, отображающее форму редактирования существующего обьекта, повторное отображение формы с ошибками проверки и сохранение изменений в обьекте.
"""

class CustomUpdateView(generic.UpdateView):
    model = Author
    fields = '__all__'
    template_name = 'create-view.html'
    success_url = '/views/View'


"""
9. DeleteView

Представление, отображающее страницу подтверждения и удаляющее существующий обьект.
"""


class CustomDeleteView(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('class-view')
    template_name = 'form-view.html'


"""
10. ArchiveIndexView

Индексная страница вернего уровня, показывающая последние обьекты по дате.
Обьекты с датой в будущем не включаются (allow_future).

Контекст:
    - date_list - QuerySet обьект, содержащий все годы, в которых есть обьекты.
"""

class CustomArchiveIndexView(generic.ArchiveIndexView):
    model = Book
    date_field = 'pubdate'
    template_name = 'object-list.html'


"""
11. YearArchiveView


Страница годового архива, показывающая все доступные месяцы в данном году.
Обьекты с датой в будущем не отображаются (allow_future).

Атрибуты:
    - make_object_list - следует ли получить полный список обьектов за этот год и передать его в шаблон.
    - get_make_object_list - будет ли возвращен список обьектов как часть контекста.
Контекст:
    - date_list - то же.
    - year - date обьект, представляющий данный год.
    - next_year - date обьект, представляющий первый день след. года в соотв. с allow_empty и allow_future.
    - previous_year - date обьект, представляющий первый день предыдущего года в соотв. с allow_empty и allow_future.
"""

class CustomYearArchiveView(generic.YearArchiveView):
    queryset = Book.objects.all()
    date_field = 'pubdate'
    make_object_list = True
    template_name = 'object-list.html'
    allow_future = True
    # year = date(2023, 1, 1)


"""
12. MonthArchiveView

Страница ежемесячного архива, показывающая все обьекты за определенный месяц.
"""

class CustomMonthArchiveView(generic.MonthArchiveView):
    template_name = 'object-list.html'
    queryset = Book.objects.all()
    date_field = 'pubdate'
    month_format = '%m'
    allow_future = True


"""
13. WeekArchiveView

Страница еженедельного архива, показывающая все обьекты за данную неделю.
"""

class CustomWeekArchiveView(generic.WeekArchiveView):
    template_name = 'object-list.html'
    queryset = Book.objects.all()
    date_field = 'pubdate'
    week_format = '%W'


"""
14. DayArchiveView

Страница архива дня, показывающая все обьекты за определенный день.
"""

class CustomDayArchiveView(generic.DayArchiveView):
    template_name = 'object-list.html'
    queryset = Book.objects.all()
    date_field = 'pubdate'


"""
15. TodayArchiveView

Страница архива дня, показывающая все обьекты за сегодня.
"""

class CustomTodayArchiveView(generic.TodayArchiveView):
    template_name = 'object-list.html'
    queryset = Book.objects.all()
    date_field = 'pubdate'


"""
16. DateDetailView

Страница, представляющая отдельный обьект.
"""

class CustomDateDetailView(generic.DateDetailView):
    template_name = 'object.html'
    model = Book
    date_field = 'pubdate'
