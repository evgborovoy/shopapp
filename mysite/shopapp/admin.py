from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from shopapp.models import Product, Order
from shopapp.admin_mixins import ExportAsCSVMixin


# Для выполнения групповых действий с объектами
@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    ordering = ["pk"]
    list_display = ["pk", "name", "price", "discount", "description", "archived"]
    list_display_links = ["pk", "name"]
    search_fields = ["pk", "name", "description"]
    inlines = [OrderInline]
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",  # Mixin для импорта данных в csv файле
    ]
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
        }),
        ("Extra", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra option 'archived' is for soft delete",
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 60:
            return obj.description
        return obj.description[:60] + "..."


class ProductInline(admin.TabularInline):
    # Для редактирования встроенных связей в админке через ManyToMany
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk", "delivery_address", "promocode", "created_at", "user_verbose"]
    inlines = [ProductInline]
    search_fields = ["pk", "created_at", "user__first_name", "user__last_name"]

    # Для оптимизации запросов к БД. Поле user загрузится для всех за 1 раз, а не по количеству записей
    def query_set(self, request):
        return Order.objects.select_relateed("user").prefetch_related("products")

    #
    def user_verbose(self, obj: Order) -> str:
        return f"{obj.user.first_name} {obj.user.last_name}" or obj.user.username
