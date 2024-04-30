from django.core import validators
from django.db import models

from sales.validators import inn_validator


# Create your models here.


class DecisionMaker(models.Model):
    """ Лицо принимающее решение (Представитель Клиента) """

    first_name = models.CharField(max_length=70, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=70, verbose_name="Фамилия", null=True, blank=True)
    middle_name = models.CharField(max_length=70, verbose_name='Отчество', null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Должность', null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', null=True)
    email = models.EmailField(verbose_name="email", null=True, blank=True)
    birthdate = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    @property
    def initials(self):
        if self.last_name:
            initials = self.last_name + f" {self.first_name[0].title()}." if self.first_name else ""
            if self.first_name and self.middle_name:
                initials += f"{self.middle_name[0].title()}."
            return initials

    def __str__(self):
        if self.initials:
            return self.initials + f" {self.title}" if self.title else ""
        else:
            return super().__str__()


class CustomerStatus(models.Model):
    """ Статус клиента (Этап) """

    title = models.CharField(max_length=50)
    progress = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)])

    class Meta:
        ordering = ('progress', )

    def __str__(self):
        return self.title


class Customer(models.Model):
    """ Клиент """

    SOURCE_CHOICES = (
        ('search', 'Поиск'),
        ('exhibition', 'Выставка'),
        ('recommendation', 'Рекомендация'),
        ('website', 'Сайт'),
        ('call', 'Звонок'),
    )

    PURCHASE_METHOD_CHOICES = (
        ('tender', 'Тендер'),
        ('free', 'Свободный'),
        ('demand', 'По потребности'),
        ('quarterly', 'Квартальный'),
    )

    id = models.AutoField(primary_key=True, verbose_name='#')
    status = models.ForeignKey(CustomerStatus, verbose_name='Статус (Этап)', on_delete=models.PROTECT,
                               null=False, blank=False)
    status_updated_at = models.DateTimeField(verbose_name='Последнее изменение статуса', auto_now_add=True,
                                             editable=True, null=False)  # TODO: Нереализованная функциональность

    inn = models.CharField(max_length=12, validators=[inn_validator], verbose_name='ИНН',
                           unique=True, null=False, blank=False)
    name = models.CharField(max_length=200, verbose_name='Наименование', null=False, blank=False)
    decision_maker = models.OneToOneField(DecisionMaker, verbose_name='ЛПР', on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=15, verbose_name='Способ привлечения', choices=SOURCE_CHOICES,
                              null=True, blank=True)
    total_volume = models.IntegerField(verbose_name='Общий объем', help_text='тыс. м2', null=True, blank=True)
    target_volume = models.IntegerField(verbose_name='Целевой объем', help_text='тыс. м2', null=True, blank=True)
    current_supplier = models.CharField(verbose_name='Действующий поставщик', max_length=200, null=True, blank=True)
    consumed_items = models.TextField(verbose_name='Потребляемая номенклатура')

    problematic = models.TextField(verbose_name='Возражения/проблематика')
    purchase_method = models.CharField(max_length=15, verbose_name='Способ закупки', choices=PURCHASE_METHOD_CHOICES,
                                       null=True, blank=True)
    note = models.TextField(verbose_name='Примечания')

    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, editable=False, null=False)
    updated_at = models.DateTimeField(verbose_name='Изменено', auto_now_add=True, editable=True, null=False)