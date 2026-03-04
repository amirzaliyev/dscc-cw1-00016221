from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    RESTRICT,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
)


class Customer(Model):
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    is_vip = BooleanField(default=False)
    created_by = ForeignKey(
        get_user_model(), on_delete=SET_NULL, related_name="customers", null=True
    )

    def __str__(self) -> str:
        return f"{self.full_name} {self.phone_number}"

    def __repr__(self) -> str:
        return f"<User(full_name={self.full_name}, phone_number={self.phone_number})>"


class Tag(Model):
    name = CharField(max_length=255)
    created_by = ForeignKey(
        get_user_model(), on_delete=SET_NULL, related_name="tags", null=True
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Tag(name={self.name})>"


class Product(Model):
    name = CharField(max_length=255)
    sku_code = CharField(max_length=30, unique=True)
    tags = ManyToManyField("sales.Tag", related_name="products", blank=True)
    created_by = ForeignKey(
        get_user_model(), on_delete=SET_NULL, related_name="products", null=True
    )

    def __str__(self) -> str:
        return f"{self.name} {self.sku_code}"

    def __repr__(self) -> str:
        return f"<Product(name={self.name}, sku_code={self.sku_code})>"


class Order(Model):
    total_amount = DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = DateTimeField(auto_now_add=True)
    customer = ForeignKey(
        "sales.Customer", on_delete=SET_NULL, related_name="orders", null=True
    )
    created_by = ForeignKey(
        get_user_model(), on_delete=SET_NULL, related_name="orders", null=True
    )

    def __str__(self) -> str:
        return f"Order(total_amount={self.total_amount})"


class OrderItem(Model):
    product = ForeignKey("sales.Product", on_delete=RESTRICT, related_name="+")
    order = ForeignKey("sales.Order", on_delete=CASCADE, related_name="items")
    quantity = IntegerField()
    price = DecimalField(max_digits=15, decimal_places=2)
