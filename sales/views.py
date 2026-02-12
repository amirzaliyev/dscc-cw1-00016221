from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from sales.forms import CustomerForm, OrderForm, OrderItemFormSet
from sales.models import Order

# def register(request: HttpRequest):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#
#     else:
#         form = RegistrationForm()
#
#     return render(request, "registration/register.html", context={"form": form})


@login_required
def home(request: HttpRequest):
    context = {"user": request.user}
    return render(request, "home.html")


@login_required
def list_orders(request: HttpRequest):
    context = {"order_list": Order.objects.all()}
    return render(request, "sales/order_list.html", context)


@login_required
def create_order(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            return redirect("order_list")
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(
        request, "sales/order_form.html", context={"form": form, "formset": formset}
    )


@login_required
def get_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "sales/order_detail.html", context={"order": order})


@login_required
def update_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("order_detail", pk=pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(
        request, "sales/order_form.html", context={"form": form, "formset": formset}
    )


@login_required
def delete_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")

    return render(request, "sales/order_confirm_delete.html", context={"order": order})


@login_required
def create_customer(request: HttpRequest):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({"id": customer.id, "name": str(customer)})
        return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)
