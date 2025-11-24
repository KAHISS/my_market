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
    in_catalog = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='inventory/covers/%Y/%m/%d/', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.name


class Stock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.product.name

        # 🏷️ Preço com desconto
    def get_discounted_price(self):
        """
        Retorna o preço de venda com desconto aplicado.
        """
        price = self.sale_price
        if self.discount:
            price -= (self.discount / 100) * price
        return round(price, 2)

    # 📦 Preço por embalagem
    def get_price_packaging(self):
        """
        Retorna o preço do lote considerando o número de unidades por embalagem.
        """
        base_price = self.get_discounted_price()
        return round(base_price * self.product.unit_per_packaging, 2)

    # 💰 Total por quantidade
    def get_total_price(self, quantity, unit_type="unit", discount=None):
        """
        Retorna o preço total do produto com base na quantidade e tipo de unidade.
        """
        total_units = quantity * \
            self.product.unit_per_packaging if unit_type == "packaging" else quantity
        price_per_unit = self.sale_price

        # aplica desconto adicional, se houver
        if discount:
            price_per_unit -= (discount / 100) * price_per_unit
        elif self.discount:
            price_per_unit -= (self.discount / 100) * price_per_unit

        total = total_units * price_per_unit
        return round(total, 2)

    # 🔻 Reduz estoque
    def reduce_stock(self, quantity, unit_type="unit"):
        """
        Reduz a quantidade do estoque.
        """
        total_units = quantity * \
            self.product.unit_per_packaging if unit_type == "packaging" else quantity
        self.quantity = max(0, self.quantity - total_units)
        self.save()
