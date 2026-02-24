from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from sales.models import Customer, Order, OrderItem, Product, Tag


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ["full_name", "phone_number", "is_vip"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["name", "sku_code"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["total_amount", "customer"]
    readonly_fields = ["total_amount"]
    inlines = [OrderItemInline]

    def save_related(
        self, request: HttpRequest, form: Any, formsets: Any, change: Any
    ) -> None:
        super().save_related(request, form, formsets, change)
        order = form.instance
        order.total_amount = sum(
            item.quantity * item.price for item in order.items.all()
        )
        order.save(update_fields=["total_amount"])
