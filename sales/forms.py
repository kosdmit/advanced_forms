from typing import Optional

from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms

from sales.models import Customer, DecisionMaker, CustomerStatus


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
            label=self._meta.model.status.field.verbose_name
        )
        self.fields['status'] = status

        # Добавляем поля DecisionMakerForm
        self.fields.update(DecisionMakerForm().fields)
        # Если есть объект, то добавляем для отображения атрибуты decision_maker
        if self.instance and self.instance.decision_maker:
            self.initial.update(**self.instance.decision_maker.__dict__)

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