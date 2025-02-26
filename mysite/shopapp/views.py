from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from shopapp.models import Product, Order


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "shopapp/products-list.html", context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, "shopapp/orders-list.html", context)
