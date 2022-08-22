from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import *
from .forms import OrderForm, RegistrationForm, LoginForm, CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.
@unauthenticated_user
def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username} successfully !!!")
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {
        "title": "Registration",
        "form": form,
    }
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, "User Logged In !!!")
            return redirect(request.GET['next'] if "next" in request.GET else "user_page")
    else:
        form = LoginForm()
    context = {
        "title": "Login",
        "form": form
    }
    return render(request, "accounts/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "customer"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "title": "User Page",
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending

    }
    return render(request, "accounts/user.html", context)


@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "title": "DashBoard",
        "orders": orders,
        "customers": customers,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending

    }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@admin_only
def show_products(request):
    products = Product.objects.all()
    context = {
        "title": "Products",
        "products": products
    }
    return render(request, "accounts/products.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def get_customer_data(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {
        "title": "Customer Data",
        "customer": customer,
        'orders': orders,
        "order_count": order_count,
        "myfilter": myfilter
    }
    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status"))
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Order Created Successfully !!!")
            return redirect("home")
    else:
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
        # form = OrderForm(initial={"customer": customer})
    context = {
        "title": "Create Order",
        "formset": formset
    }
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.info(request, "Order Updated Successfully !!!")
            return redirect("home")
    else:
        form = OrderForm(instance=order)
    context = {
        "title": "Update Order",
        "form": form
    }
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == "POST":
        order.delete()
        messages.error(request, "Order Deleted Successfully !!!")
        return redirect("home")
    context = {
        "title": "Delete Order",
        "order": order
    }
    return render(request, "accounts/delete_order.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def account_settings(request):
    customer = request.user.customer
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    else:
        form = CustomerForm(instance=customer)
    context = {"form": form}
    return render(request, "accounts/account_settings.html", context)
