from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário", related_name='client_profile')
    type = models.CharField("Tipo", choices=[(
        'PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], default='PF', blank=True, null=True)
    document = models.CharField(
        "CPF/CNPJ", max_length=14, unique=True, blank=True, null=True)
    credit = models.DecimalField(
        "Crédito", max_digits=10, decimal_places=2, default=0.00)
    phone = models.CharField("Telefone", max_length=15, blank=True, null=True)
    address = models.CharField(
        "Endereço", max_length=255, blank=True, null=True)
    address_number = models.IntegerField("Número", blank=True, null=True)
    address_neighborhood = models.CharField(
        "Bairro", max_length=255, blank=True, null=True)
    address_city = models.CharField(
        "Cidade", max_length=255, blank=True, null=True)
    address_state = models.CharField(
        "Estado", max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(
        "CEP", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.user.username}"
