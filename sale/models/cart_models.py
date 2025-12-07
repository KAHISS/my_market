from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


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
