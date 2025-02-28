from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shopapp.models import Product, Order
from shopapp.forms import ProductForm, OrderForm


class ProductsListView(ListView):
    model = Product
    # queryset = Product.objects.filter(archived=False) # If only 'available' products are needed
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    form_class = ProductForm  # Can leave it if 'fields' is use


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "price", "description", "discount"]  # Fields that need to be edited
    template_name_suffix = "_update_form"

    # To use the parameters when the update is successful
    def get_success_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    # Do not delete, but set 'archived' = true
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")
    context_object_name = "orders"


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
    form_class = OrderForm


class OrderUpdateView(UpdateView):
    model = Order
    fields = ["delivery_address", "products", "user"]
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


@login_required
def create_order(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    return render(request, "shopapp/order_form.html", context=context)
