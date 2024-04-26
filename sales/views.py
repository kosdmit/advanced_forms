from django.views.generic import CreateView

from sales.forms import CustomerForm
from sales.models import Customer


# Create your views here.


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
