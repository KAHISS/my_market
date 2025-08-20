import uuid
from django.db import models

class Product(models.Model):
    """
    Representa um produto no sistema.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Retorna uma o nome do produto.
        """
        return self.nome
    
class StockMovement(models.Model):
    """
    Registra todas as entradas e saídas de um produto do estoque.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10)
    quantity = models.IntegerField()
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Retorna todas as entradas e saídas de um produto do estoque.
        """
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"
