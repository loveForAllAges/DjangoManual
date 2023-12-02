"""
Работа с формами


Каждое поле формы имеет класс Widget.
Как только данные формы будут проверены (is_valid()), они будут в form.cleaned_data словаре.

Параметры рендеринга формы:
    - form.as_div - форма в тегаъ div.
    - form.as_table - форма в тегах tr.
    - form.as_p - форма в тегах p.
    - form.as_ul - форма в тегах li.

Атрибуты field:
    - field.errors - ошибки поля.
    - field.label_tag - тэг поля.
    - field.field - поле.
    - field.help_text - справочный текст поля.
    - field.html_name - имя поля.
    - field.id_for_label - id поля.
    - field.is_hidden - является ли скрытым полем.
    - field.label - метка поля.
    - field.legend_tag - аналогично label_tag, но использует тег legeng.
    - field.user_fieldset - содержит ли несколько входных данных для группировки.
    - field.value - значение поля.

form.hidden_fields - невидимые поля.
form.visible_fields - видимые поля.
form.non_field_erorrs - ошибки формы не привязанные к полям.

TODO:
1. https://docs.djangoproject.com/en/4.2/topics/forms/formsets/
2. https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
3. https://docs.djangoproject.com/en/4.2/topics/forms/media/
"""