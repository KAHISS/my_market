import uuid
from django.db import models


class Category(models.Model):
    """
    Represent a category of products.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        """
        Return the name of the category.
        """
        return self.name


class Product(models.Model):
    """
    Represent a product in the inventory.
    """
    barcode = models.CharField(
        max_length=13, blank=True, null=True, unique=True)
    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    packaging_type = models.CharField(
        max_length=64, blank=True, null=True, default="Caixa")
    unit_measure = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        choices=[
            ("UN", "Unidade"),
            ("L", "Litro"),
            ("KG", "Kilograma"),
            ("G", "Grama"),
            ("ML", "Mililitro"),
            ("GR", "Grão"),
        ],
        default="UN"
    )
    unit_per_packaging = models.IntegerField(default=1)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    minimum_stock = models.IntegerField(default=0)
    stock_quantity = models.IntegerField(default=0)
    in_catalog = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='inventory/covers/%Y/%m/%d/', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.name

    def get_discounted_price(self):
        """
        Return the discounted price of the product.
        """
        if self.discount:
            return f"{self.sale_price - (self.discount / 100 * self.sale_price):.2f}".replace(".", ",")
        return f"{self.sale_price:.2f}".replace(".", ",")

    def get_price_packaging(self):
        """
        Return the price of the product per packaging.
        """
        if self.discount:
            return f"{(self.sale_price - (self.discount / 100 * self.sale_price)) * self.unit_per_packaging:.2f}".replace(".", ",")
        return f"{self.sale_price * self.unit_per_packaging:.2f}".replace(".", ",")

    def get_total_price(self, quantity, unit_type="unit", discount=None):
        """
        Return the price of the product based on the quantity and unit type.
        """
        total_units = quantity * self.unit_per_packaging if unit_type == "packaging" else quantity
        if discount:
            return f"{total_units * self.sale_price - (discount / 100 * total_units * self.sale_price):.2f}".replace(".", ",")
        return f"{total_units * self.sale_price:.2f}".replace(".", ",")

    def reduce_stock(self, quantity, unit_type="unit"):
        """
        Reduce the stock quantity of the product.
        """
        if unit_type == "packaging":
            quantity *= self.unit_per_packaging
        self.stock_quantity -= quantity
        self.save()
