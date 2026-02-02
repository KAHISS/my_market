from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product

# Create your models here.


class Sale(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Vendedor")
    client = models.CharField(
        "Cliente", max_length=255, default='Consumidor Final', blank=True)
    total_quantity = models.PositiveIntegerField("Quantidade Total", default=0)
    subtotal = models.DecimalField(
        "Subtotal", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(
        "Desconto", max_digits=10, decimal_places=2, default=0)
    freight = models.DecimalField(
        "Frete", max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(
        "Total", max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        "Status", max_length=50,
        default='pendente',
        choices=[
            ('pendente', 'Pendente'),
            ('pago', 'Pago'),
            ('cancelado', 'Cancelado'),
            ('saida', 'Saída')
        ]
    )
    payment_method = models.CharField(
        "Método de Pagamento", max_length=255,
        default='sem pagamento',
        choices=[
            ('sem pagamento', 'Sem Pagamento'),
            ('dinheiro', 'Dinheiro'),
            ('cartão', 'Cartão'),
            ('pix', 'Pix'),
        ]
    )
    cash_received = models.DecimalField(
        "Valor Recebido", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return f'Venda #{self.id} - {self.seller}'

    def get_total_quantity(self):
        self.total_quantity = sum(
            item.quantity for item in self.sale_items.all())
        self.save()

    def get_subtotal(self):
        self.subtotal = sum(item.subtotal for item in self.sale_items.all())
        self.save()

    def get_total_price(self):
        self.total_price = self.subtotal - self.discount + self.freight
        self.save()


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name='sale_items', verbose_name="Venda")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    subtotal = models.DecimalField(
        "Subtotal", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_subtotal(self):
        stock = getattr(self.product, 'stock', None)
        if stock:
            self.subtotal = stock.sale_price * self.quantity
            self.save()
