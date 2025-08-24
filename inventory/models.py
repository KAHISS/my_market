import uuid
from django.db import models


class Category(models.Model):
    """
    Represent a category of products.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Return the name of the category.
        """
        return self.name


class Product(models.Model):
    """
    Represent a product in the inventory.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimun_stock = models.IntegerField(default=0)
    stock_quantity = models.IntegerField(default=0)
    in_catalog = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='inventory/covers/%Y/%m/%d/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.name


class StockMovement(models.Model):
    """
    Register stock movements.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10)
    quantity = models.IntegerField()
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Return the name of the product and the movement type.
        """
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"
