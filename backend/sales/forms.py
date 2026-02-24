from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory

from sales.models import Customer, Order, OrderItem


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["full_name", "phone_number", "is_vip"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer"]


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=["product", "quantity", "price"], extra=1
)


class RegistrationForm(UserCreationForm):
    pass
