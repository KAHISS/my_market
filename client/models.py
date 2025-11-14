from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    type = models.CharField(choices=[(
        'PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], default='PF', blank=True, null=True)
    document = models.CharField(
        max_length=14, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    address_number = models.IntegerField(blank=True, null=True)
    address_neighborhood = models.CharField(
        max_length=255, blank=True, null=True)
    address_city = models.CharField(max_length=255, blank=True, null=True)
    address_state = models.CharField(max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='client/covers/%Y/%m/%d/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
