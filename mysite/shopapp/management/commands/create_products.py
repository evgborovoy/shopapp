from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")
        products = [
            ["Table", 239, 0, "Big wooden table"],
            ["Lamp", 59, 10, "Small white lamp"],
            ["Bluetooth speaker", 119, 5, "Mid size speaker"],
        ]
        for product in products:
            product, created = Product.objects.get_or_create(
                name=product[0],
                price=product[1],
                discount=product[2],
                description=product[3]
            )
            self.stdout.write(f"Created product {product.name}")

        self.stdout.write(self.style.SUCCESS("Products created"))
