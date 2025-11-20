from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carinho de {self.user.username}"

    def total_price(self):
        return sum(item.subtotal() for item in self.cart_items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())

    def total_discount(self):
        return sum(item.discount() for item in self.cart_items.all())

    def total_price_with_discount(self):
        return self.total_price() - self.total_discount()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

    def subtotal(self):
        stock = getattr(self.product, 'stock', None)
        if stock:
            return stock.sale_price * self.quantity

    def discount(self):
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

    def percentage_discount(self):
        discount = ((self.subtotal() - self.discount()) /
                    self.subtotal() * 100) - 100
        return f"{discount:.1f}"

    def total_price_with_discount(self):
        return self.subtotal() - self.discount()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_client')
    seller = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='order_seller')
    status = models.CharField(
        max_length=50,
        default='pendente',
        choices=[
            ('pendente', 'Pendente'),
            ('em_separacao', 'Em separação'),
            ('em_transporte', 'Em transporte'),
            ('entregue', 'Entregue'),
            ('pago', 'Pago'),
            ('cancelado', 'Cancelado'),
        ]
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price_with_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
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
