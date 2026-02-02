from django.db import models
from django.contrib.auth.models import User


class Kind(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de despesa"
        verbose_name_plural = "Tipos de despesas"

    def __str__(self):
        return self.name


class Expense(models.Model):
    class Modality(models.TextChoices):
        RETAIL = "R", "Varejo"
        WHOLESALE = "W", "Atacado"
        OTHER = "O", "Outro"

    class Status(models.TextChoices):
        PENDING = "P", "Pendente"
        PAID = "D", "Pago"
        CANCELLED = "C", "Cancelado"

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = "C", "Cartão de crédito"
        DEBIT_CARD = "D", "Cartão de débito"
        CASH = "M", "Dinheiro"
        BANK_TRANSFER = "B", "Transferência bancária"

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    modality = models.CharField(max_length=1, choices=Modality.choices)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)
    pay_by = models.DateField(
        verbose_name="Data de vencimento", null=True, blank=True)
    payday = models.DateField(
        verbose_name="Data do pagamento", null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor")
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(
        max_length=1, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    observation = models.TextField(
        verbose_name="Observação", null=True, blank=True)
    proof = models.ImageField(
        "Comprovante", upload_to='finances/proofs/%Y/%m/%d/', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"

    def __str__(self):
        return f"{self.modality} - {self.kind.name}"
