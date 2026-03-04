from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from sales.forms import (
    CustomerForm,
    OrderForm,
    OrderItemFormSet,
    ProductForm,
    RegistrationForm,
)
from sales.models import Order, Product


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", context={"form": form})


@login_required
def home(request: HttpRequest):
    context = {"user": request.user}
    return render(request, "home.html")


@login_required
def list_orders(request: HttpRequest):
    context = {"order_list": Order.objects.filter(created_by=request.user)}
    return render(request, "sales/order_list.html", context)


def _apply_product_queryset(formset, user):
    qs = Product.objects.filter(created_by=user)
    for form in formset.forms:
        form.fields["product"].queryset = qs


@login_required
def create_order(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST, user=request.user)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            order.total_amount = sum(
                item.price * item.quantity for item in order.items.all()
            )
            order.save()
            return redirect("order_list")
    else:
        form = OrderForm(user=request.user)
        formset = OrderItemFormSet()

    _apply_product_queryset(formset, request.user)
    return render(
        request, "sales/order_form.html", context={"form": form, "formset": formset}
    )


@login_required
def get_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk, created_by=request.user)
    return render(request, "sales/order_detail.html", context={"order": order})


@login_required
def update_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order, user=request.user)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.total_amount = sum(
                item.price * item.quantity for item in order.items.all()
            )
            order.save()
            return redirect("order_detail", pk=pk)
    else:
        form = OrderForm(instance=order, user=request.user)
        formset = OrderItemFormSet(instance=order)

    _apply_product_queryset(formset, request.user)
    return render(
        request, "sales/order_form.html", context={"form": form, "formset": formset}
    )


@login_required
def delete_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk, created_by=request.user)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")

    return render(request, "sales/order_confirm_delete.html", context={"order": order})


@login_required
def create_customer(request: HttpRequest):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return JsonResponse({"id": customer.id, "name": str(customer)})
        return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)


@login_required
def create_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return JsonResponse({"id": product.id, "name": str(product)})
        return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)
