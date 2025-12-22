from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product

# Create your models here.


class Sale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        default='pendente',
        choices=[
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
            ('cancelado', 'Cancelado'),
        ]
    )
    payment_method = models.CharField(max_length=255, default='dinheiro')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.seller} - {self.total_price}'


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percentage_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_subtotal(self):
        stock = getattr(self.product, 'stock', None)
        if stock:
            self.subtotal = stock.sale_price * self.quantity
            self.save()

    def get_discount(self):
        stock = getattr(self.product, 'stock', None)
        if not stock:
            return 0

        units_per_pack = self.product.unit_per_packaging or 1
        full_packs = self.quantity // units_per_pack  # pacotes completos

        if full_packs == 0:
            return 0  # ainda não tem desconto

        discount_per_pack = (stock.sale_price -
                             stock.wholesale_price) * units_per_pack
        total_discount = full_packs * discount_per_pack

        return total_discount

    def get_percentage_discount(self):
        discount = ((self.subtotal - self.discount) /
                    self.subtotal * 100) - 100
        return f"{discount:.1f}"

    def get_total_price(self):
        self.total_price = self.subtotal - self.discount
        self.save()
