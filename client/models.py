from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, default=None, verbose_name="Usuário", null=True, blank=True)
    first_name = models.CharField(
        "Nome", max_length=255, blank=True, null=True)
    last_name = models.CharField(
        "Sobrenome", max_length=255, blank=True, null=True)
    type = models.CharField("Tipo", choices=[(
        'PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], default='PF', blank=True, null=True)
    document = models.CharField(
        "CPF/CNPJ", max_length=14, unique=True, blank=True, null=True)
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
        return self.first_name + ' ' + self.last_name
