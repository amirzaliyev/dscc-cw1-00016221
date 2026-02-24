from django.urls import path

from sales.views import (
    create_customer,
    create_order,
    delete_order,
    get_order,
    list_orders,
    update_order,
)

urlpatterns = [
    path("", list_orders, name="order_list"),
    path("create", create_order, name="order_create"),
    path("<int:pk>/", get_order, name="order_detail"),
    path("<int:pk>/update", update_order, name="order_update"),
    path("<int:pk>/delete", delete_order, name="order_delete"),
    path("customers/create", create_customer, name="customer_create"),
]
