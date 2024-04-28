from django import forms

from sales.models import Customer


class CustomerForm(forms.ModelForm):
    template_name_div = 'forms/div.html'

    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        