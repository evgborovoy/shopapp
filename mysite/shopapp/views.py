from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from shopapp.models import Product


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "shopapp/products-list.html", context)
