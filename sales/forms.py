from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory

from sales.models import Order, OrderItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer"]


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=["product", "quantity", "price"], extra=1
)


class RegistrationForm(UserCreationForm):
    pass
