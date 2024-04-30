# Продвинутое использование форм в Django (на примере Bootstrap и crispy)

## Введение

Хотя в настоящее время большой популярностью пользуется клиентский рендеринг веб-интерфейсов, Django с «батарейками» в комплекте предоставляет широкий функционал для server-side рендеринга, который позволяет быстро реализовывать интерфейсы решающие задачи бизнеса.

В этой статье я хочу поговорить о существующих подходах к рендерингу веб-форм в Django.

## Проблема

Для демонстрации будем использовать простую модель:

###### _models.py_

````python
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
````

Для работы с формами Django предоставляет модуль forms включающий мета классы, которые позволяют декларативно cгенерировать форму для нашей модели:

###### _forms.py_

```
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
```

Создадим простое представление для демонстрации получаемых форм:

###### _views.py_

```
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
```

Добавим форму в шаблон html страницы:

###### _customer_form.html_

```python
{% extends 'base.html' %}

{% block content %}
  {{ form }}
{% endblock %}
```

Поздравляю! Нам потребовалось ровно 4 строчки кода чтобы отрендерить форму включающиую множество полей и одна строка, чтобы добавить ее в шаблон (не считаем создание конечной точки http). Но согласитесь, в текущем варинате форма смотрится крайне аскетично:

![1.PNG](assets/1.PNG)

* [ ]  Отсутвует стилизация форм
* [X]  Форма генерируется автоматически

Django еще не знает, что мы используем css-фреймфорк Bootstrap 5 (хотя вы можете использовать любой другой) для стилизации html страниц.

## Наивное решение

Bootstrap предоставляет широкий набор классов и готовых снипетов форм для использования в шаблонах. Первое решение котрое приходит на ум: "Давайте добавим нужные элементы прямо в шаблон!".

В таком случае мы берем написание html кода формы на себя, используя сниппеты предоставляемые css библиотекой. Таким образом можно добиться безупречной стилизации формы, контролируя каждый элемент в отдельности. Но есть и недостатки такого подхода. Из одной строки вида: `{{ form }}`, форма разрастается до десятков и даже сотен строк. Мы вынуждены контролировать виджеты, лэйблы, строки подсказок, вывод ошибок и многе другое. При этом переиспользование и поддержка при таком подходе крайне затруднены, поскольку форма создается индивидуально, под конкретную реализацию.

* [X]  Контролируем стилизацию и шаблон формы
* [ ]  Пишем html шаблон формы вручную под конкретную реализацию

Что то здесь не так, ведь на предыдущем этапе мы задействовали встроенные механизмы рендеринга форм Django, не будем от них отказываться!

## Трудоемкое решение

Согласно докуметации для применения стилей Bootstrap элемент `<input>` должен иметь класс `form-label`. Мы можем переопределить поля генерируемые мета классом forms.ModelForm с помощью переменных класса, инициализировав для них виджеты с необходимым атрибутом, например:

```python
 name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
```

Правда тогда, нам нужно опрделить все атрибуты поля самостоятельно, т.к. созданный объект поля переопределит генеруемый автоматически. Поэтому лучше расширить метод `__init__`:

###### *forms.py*

```python
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
```

Мы используем встроенные механизмы генерации объявленных полей вызвая родительский метод `__init__()` внутри переопределнного инициализатора формы, после чего в цикле для каджого виджета поля, добавляем ключ-значение `'class': 'form-control'` в словарь `widget.attrs`. Django будет использовать атрибут `attrs` при рендеринге элемента `<input>`, таким образом мы получим желаемый результат.

Если стилизации элемента `<input>` недостаточно, и необходимо изменять html структуру формы, то можно прибегнуть к другому инструменту. Мета классы форм в Django позволяют переопределить шаблоны используемые для рендеринга c помошью переменных класса вида template_name_* (например template_name_div или template_name_label в зависимотси от переопределяемого шаблона). Таким образом мы сможем отказаться от определения html кода каждой формы вручную в пользу переопределения многократно используемых шаблонов.

Поставляемые с фреймворком шаблоны хранятся в следующей директории: `venv/Lib/site-packages/django/forms/templates/django/forms`.

Bootstrap использует верстку форм на основе div'ов поэтому за основу нового шаблона возьмем `forms/div.html`. Изменим шаблон для соответсвия сниппету Bootstrap:

###### *div.html*

```
...
{% for field, errors in fields %}
  <div {% with classes=field.css_classes %}class="form-floating mb-3 {{ classes }}"{% endwith %}>
    {{ errors }}
    {{ field }}
    {% if field.use_fieldset %}
      <fieldset>
      {% if field.label %}{{ field.legend_tag }}{% endif %}
    {% else %}
      {% if field.label %}{{ field.label_tag }}{% endif %}
    {% endif %}
    {% if field.help_text %}<div class="form-text">{{ field.help_text|safe }}</div>{% endif %}
    {% if field.use_fieldset %}</fieldset>{% endif %}
    {% if forloop.last %}
      {% for field in hidden_fields %}{{ field }}{% endfor %}
    {% endif %}
</div>
{% endfor %}
...
```

![2.PNG](assets/2.PNG)

Таким образом получен отличный результат, мы сохранили минимальстичность шаблона страницы и инкапсульровали рендеринг формы в соответсвующий класс, при этом используя встроенные механизмы генарции форм для Django моделей.

Но есть и недостатки: мы вынуждены создавать новые шаблоны для конкретных реализаций форм.

* [X]  Контролируем стилизацию и шаблон формы
* [X]  Генерируем html шаблон автоматически

Как это часто бывает, сообщество Python предлагает готовое решение для продвинутого рендеринга форм в Django.

## Готовое решение

Одно из наиболее популярных решений для рендеринга форм в джанго - пакет **[django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)** (4.9 тыс. звезд на GitHub). Пакет поволяет подключать и использовать готовые библиотеки шаблонов для различных фронтенд фреймворков например [Bootstrap](https://getbootstrap.com/), [tailwind](https://github.com/django-crispy-forms/crispy-tailwind), [Bulma](https://github.com/ckrybus/crispy-bulma) и др.

Пакет предоставлеят мощные инструменты для генерации всевозмоных вариантов представления формы. Подробнее о всех возможностях crispy вы можете ознакомится в [официальной документации](https://django-crispy-forms.readthedocs.io/en/latest/index.html). Здесь лишь приведу пример формы из реального проекта:

```
class DecisionMakerForm(forms.ModelForm):
    class Meta:
        model = DecisionMaker
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    FIELD_GROUPS = {
        'main': ('status', 'inn', 'name'),
        'decision_maker': (*DecisionMakerForm().fields.keys(), 'source'),
        'shipment': ('total_volume', 'target_volume', 'current_supplier',
                     'consumed_items', 'problematic', 'purchase_method'),
        'other': ('note', ),
    }

    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, form_action: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)

        status = forms.ModelChoiceField(
            initial=CustomerStatus.objects.first(),
            required=True,
            queryset=CustomerStatus.objects.all(),
            label=self._meta.model.status.field.verbose_name,
        )
        self.fields['status'] = status

        # Добавляем поля DecisionMakerForm
        self.fields.update(DecisionMakerForm().fields)

        # Добавляем атрибут helper для рендеринга формы с помощью crispy
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-form'
        self.helper.form_method = 'post'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            Fieldset('', *self.FIELD_GROUPS['main']),
            Accordion(AccordionGroup('ЛПР', *self.FIELD_GROUPS['decision_maker']),
                      AccordionGroup('Поставки', *self.FIELD_GROUPS['shipment']),
                      css_class='mb-3'),
            Fieldset('', *self.FIELD_GROUPS['other']),
            Submit('submit', 'Сохранить', css_class='float-end'),
        )
```

В этом примере, при инициализации объекта формы, мы добавляем атрибут `helper` который ссылается на объект класса `FormHelper` предоставляемого пакетом `crispy`. С помощью класса `FormHelper` мы можем определить html атрибуты элемента `form`, такие как метод и url ипользуемые при отправке формы. Таким образом мы инкапсулируем всю логику работы формы в соответсвующий класс не распыляя ее части по html шаблонам.

Но наибольший интерес представляет входящий в состав бибилотеки класс `Layout`. Это по настоящему мощный инструмент для конфигурирования шаблона формы. С помощью комбинирования python-объектов отображающих сниппеты bootstrap мы можем объявить сложные шаблоны форм, оставив работу по рендерингу html кода алгоритмам.

В примере мы используем группы полей (`Fieldset()`), аккордион bootstrap c двумя вкладками (обекты `Accordion()` и `AccordionGroup()`)  даже кнопку подвржедния (`Submit()`). При этом в шаблоне мы лишь определяем место расположения формы, а всю логику связанную с ней определяем в соответсвующем классе:

###### *customer_form.html*

```
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
  <div class="col-4">
    {% crispy form %}
  </div>
{% endblock %}
```

![3.PNG](assets/3.PNG)

* [X]  Контролируем стилизацию и шаблон формы

* [X]  Генерируем html шаблон автоматически

## Заключение
