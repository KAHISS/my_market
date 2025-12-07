from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_client')
    seller = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_seller', blank=True)
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
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price_with_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido de {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percentage_discount = models.DecimalField(
        max_digits=3, decimal_places=1, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_with_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"
