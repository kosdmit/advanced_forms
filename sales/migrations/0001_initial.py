# Generated by Django 5.0.4 on 2024-04-30 10:58

import django.core.validators
import django.db.models.deletion
import sales.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('progress', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'ordering': ('progress',),
            },
        ),
        migrations.CreateModel(
            name='DecisionMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=70, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=70, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=70, null=True, verbose_name='Отчество')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Должность')),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('status_updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Последнее изменение статуса')),
                ('inn', models.CharField(max_length=12, unique=True, validators=[sales.validators.inn_validator], verbose_name='ИНН')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('source', models.CharField(blank=True, choices=[('search', 'Поиск'), ('exhibition', 'Выставка'), ('recommendation', 'Рекомендация'), ('website', 'Сайт'), ('call', 'Звонок')], max_length=15, null=True, verbose_name='Способ привлечения')),
                ('total_volume', models.IntegerField(blank=True, help_text='тыс. м2', null=True, verbose_name='Общий объем')),
                ('target_volume', models.IntegerField(blank=True, help_text='тыс. м2', null=True, verbose_name='Целевой объем')),
                ('current_supplier', models.CharField(blank=True, max_length=200, null=True, verbose_name='Действующий поставщик')),
                ('consumed_items', models.TextField(verbose_name='Потребляемая номенклатура')),
                ('problematic', models.TextField(verbose_name='Возражения/проблематика')),
                ('purchase_method', models.CharField(blank=True, choices=[('tender', 'Тендер'), ('free', 'Свободный'), ('demand', 'По потребности'), ('quarterly', 'Квартальный')], max_length=15, null=True, verbose_name='Способ закупки')),
                ('note', models.TextField(verbose_name='Примечания')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Изменено')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.customerstatus', verbose_name='Статус (Этап)')),
                ('decision_maker', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.decisionmaker', verbose_name='ЛПР')),
            ],
        ),
    ]