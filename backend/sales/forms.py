from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, inlineformset_factory

from sales.models import Customer, Order, OrderItem, Product


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["full_name", "phone_number", "is_vip"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku_code"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["customer"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["customer"].queryset = Customer.objects.filter(created_by=user)


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, fields=["product", "quantity", "price"], extra=1
)


class RegistrationForm(UserCreationForm):
    pass
