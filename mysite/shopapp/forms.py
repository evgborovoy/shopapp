from django import forms

from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Price should be more then 0")
        return price


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "promocode", "products"]

    def save(self, commit=True, user=None):
        order = super().save(commit=False)
        if user:
            order.user = user
        if commit:
            order.save()
            self.save_m2m()
        return order

