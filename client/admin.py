from django.contrib import admin
from .models import Client
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    """
        Admin for Client model.
    """
    list_display = ('user', 'type', 'document', 'phone',
                    'address_neighborhood', 'address_city')


admin.site.register(Client, ClientAdmin)
