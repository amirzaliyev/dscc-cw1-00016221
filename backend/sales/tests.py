from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client

from sales.models import Customer, Order, OrderItem, Product, Tag


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="pass123")


@pytest.fixture
def client(user):
    c = Client()
    c.login(username="testuser", password="testpass123")
    return c


@pytest.fixture
def customer(user):
    return Customer.objects.create(
        full_name="John Doe", phone_number="+998901234567", created_by=user
    )


@pytest.fixture
def product(user):
    return Product.objects.create(name="Laptop", sku_code="LAP-001", created_by=user)


@pytest.fixture
def order(user, customer):
    return Order.objects.create(customer=customer, created_by=user)


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


def test_register_page_loads():
    c = Client()
    response = c.get("/accounts/register/")
    assert response.status_code == 200


def test_register_creates_user(db):
    c = Client()
    response = c.post(
        "/accounts/register/",
        {
            "username": "newuser",
            "password1": "Str0ngPass!99",
            "password2": "Str0ngPass!99",
        },
    )
    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()


def test_order_isolation(user, customer, db):
    other_user = User.objects.create_user(username="other", password="pass123")
    other_order = Order.objects.create(customer=customer, created_by=other_user)
    c = Client()
    c.login(username="testuser", password="testpass123")
    response = c.get(f"/orders/{other_order.pk}/")
    assert response.status_code == 404


# --- Customer isolation & creation ---


def test_create_customer_sets_created_by(client, user):
    response = client.post(
        "/orders/customers/create",
        {"full_name": "Jane Doe", "phone_number": "+998991234567"},
    )
    assert response.status_code == 200
    c = Customer.objects.get(full_name="Jane Doe")
    assert c.created_by == user


def test_create_customer_returns_json(client):
    response = client.post(
        "/orders/customers/create",
        {"full_name": "Jane Doe", "phone_number": "+998991234567"},
    )
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_create_customer_invalid(client):
    response = client.post("/orders/customers/create", {"full_name": ""})
    assert response.status_code == 400
    assert "errors" in response.json()


def test_create_customer_requires_login():
    c = Client()
    response = c.post(
        "/orders/customers/create",
        {"full_name": "Jane", "phone_number": "+1"},
    )
    assert response.status_code == 302


def test_order_form_only_shows_own_customers(client, user, other_user):
    Customer.objects.create(full_name="My Customer", phone_number="+1", created_by=user)
    Customer.objects.create(
        full_name="Other Customer", phone_number="+2", created_by=other_user
    )
    response = client.get("/orders/create")
    assert response.status_code == 200
    form = response.context["form"]
    qs = form.fields["customer"].queryset
    names = list(qs.values_list("full_name", flat=True))
    assert "My Customer" in names
    assert "Other Customer" not in names


# --- Product isolation & creation ---


def test_create_product_sets_created_by(client, user):
    response = client.post(
        "/orders/products/create",
        {"name": "Monitor", "sku_code": "MON-001"},
    )
    assert response.status_code == 200
    p = Product.objects.get(sku_code="MON-001")
    assert p.created_by == user


def test_create_product_returns_json(client):
    response = client.post(
        "/orders/products/create",
        {"name": "Monitor", "sku_code": "MON-002"},
    )
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_create_product_invalid(client):
    response = client.post("/orders/products/create", {"name": ""})
    assert response.status_code == 400
    assert "errors" in response.json()


def test_create_product_requires_login():
    c = Client()
    response = c.post(
        "/orders/products/create",
        {"name": "Monitor", "sku_code": "MON-003"},
    )
    assert response.status_code == 302


def test_order_form_only_shows_own_products(client, user, other_user):
    Product.objects.create(name="My Product", sku_code="MY-001", created_by=user)
    Product.objects.create(
        name="Other Product", sku_code="OT-001", created_by=other_user
    )
    response = client.get("/orders/create")
    assert response.status_code == 200
    formset = response.context["formset"]
    qs = formset.forms[0].fields["product"].queryset
    skus = list(qs.values_list("sku_code", flat=True))
    assert "MY-001" in skus
    assert "OT-001" not in skus


def test_order_list_only_shows_own_orders(client, user, other_user, customer):
    own_order = Order.objects.create(customer=customer, created_by=user)
    other_order = Order.objects.create(customer=customer, created_by=other_user)
    response = client.get("/orders/")
    assert response.status_code == 200
    order_list = response.context["order_list"]
    pks = list(order_list.values_list("pk", flat=True))
    assert own_order.pk in pks
    assert other_order.pk not in pks
