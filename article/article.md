# Продвинутое использование форм в Django

## Введение

Хотя в настоящее время большой популярностью пользуется клиентский рендеринг веб-интерфейсов, Django с «батарейками» в комплекте предоставляет широкий функционал для server-side рендеринга.

В этой статье я хочу поговорить о подходах к рендерингу форм.

## Проблема

Для демонстрации будем использовать простую модель:

###### _models_.py

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

###### _forms_.py

```
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
```

Создадим простое представление для демонстрации получаемых форм:

###### _views_.py

```
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
```

Добавим форму в шаблон html страницы:

###### _customer_form_.html

```python
{% extends 'base.html' %}

{% block content %}
  {{ form }}
{% endblock %}
```

Поздравляю! Нам потребовалось ровно 4 строчки кода чтобы отрендерить форму включающиую множество полей и одна строка, чтобы добавить ее в шаблон (не считаем создание конечной точки http). Но согласитесистесь, в текущем варинате форма смотрится крайне аскетично:

![1.PNG](assets/1.PNG)

Django еще не знает, что мы используем css-фреймфорк Bootstrap 5 (хотя вы можете использовать любой другой) для стилизации html страниц.
