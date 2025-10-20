from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    cnpj = models.CharField(max_length=14, unique=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_birth = models.DateField()
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='client/covers/%Y/%m/%d/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
