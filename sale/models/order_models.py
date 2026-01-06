from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_client', verbose_name="Cliente")
    seller = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_seller', blank=True, verbose_name="Vendedor")
    status = models.CharField(
        max_length=50,
        default='pendente',
        choices=[
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
            ('cancelado', 'Cancelado'),
        ], verbose_name="Status")
    payment_method = models.CharField(
        max_length=255, default='dinheiro', verbose_name="Método de Pagamento")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Preço Total")
    total_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Desconto Total")
    total_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Quantidade Total")
    total_price_with_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Preço Total com Desconto")
    delivered = models.BooleanField(default=False, verbose_name="Entregue")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido de {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Pedido")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    subtotal = models.DecimalField(
        "Subtotal", max_digits=10, decimal_places=2, default=0)
    percentage_discount = models.DecimalField(
        "Desconto (%)", max_digits=3, decimal_places=1, default=0)
    discount = models.DecimalField(
        "Desconto", max_digits=10, decimal_places=2, default=0)
    total_price_with_discount = models.DecimalField(
        "Preço Total com Desconto", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedido"

    def __str__(self):
        return f"{self.product.name} - Quantidade: {self.quantity}"
