from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_birth = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='client/covers/%Y/%m/%d/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name