from django.urls import path

from shopapp.views import products_list, orders_list, create_product, create_order

app_name = "shopapp"

urlpatterns = [
    path("products/", products_list, name="products_list"),
    path("products/create/", create_product, name="product_create"),
    path("orders/", orders_list, name="orders_list"),
    path("orders/create/", create_order, name="order_create"),
]
