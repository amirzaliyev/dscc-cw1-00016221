from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client

from sales.models import Customer, Order, OrderItem, Product, Tag


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def client(user):
    c = Client()
    c.login(username="testuser", password="testpass123")
    return c


@pytest.fixture
def customer(db):
    return Customer.objects.create(full_name="John Doe", phone_number="+998901234567")


@pytest.fixture
def product(db):
    return Product.objects.create(name="Laptop", sku_code="LAP-001")


@pytest.fixture
def order(customer):
    return Order.objects.create(customer=customer)


# --- Model tests ---


def test_customer_str(customer):
    assert "John Doe" in str(customer)


def test_product_tag_m2m(product):
    tag1 = Tag.objects.create(name="Electronics")
    tag2 = Tag.objects.create(name="Sale")
    product.tags.add(tag1, tag2)
    assert product.tags.count() == 2
    assert product in tag1.products.all()


def test_order_total_calculation(order, product):
    OrderItem.objects.create(
        order=order, product=product, quantity=2, price=Decimal("100.00")
    )
    OrderItem.objects.create(
        order=order, product=product, quantity=1, price=Decimal("50.00")
    )
    total = sum(item.quantity * item.price for item in order.items.all())
    assert total == Decimal("250.00")


# --- View tests ---


def test_home_redirects_anonymous():
    c = Client()
    response = c.get("/")
    assert response.status_code == 302
    assert "/accounts/login/" in response.url


def test_home_authenticated(client):
    response = client.get("/")
    assert response.status_code == 200


def test_order_list_page(client):
    response = client.get("/orders/")
    assert response.status_code == 200


def test_order_create_page(client):
    response = client.get("/orders/create")
    assert response.status_code == 200


def test_order_detail_page(client, order):
    response = client.get(f"/orders/{order.pk}/")
    assert response.status_code == 200


def test_order_delete(client, order):
    response = client.post(f"/orders/{order.pk}/delete")
    assert response.status_code == 302
    assert not Order.objects.filter(pk=order.pk).exists()
