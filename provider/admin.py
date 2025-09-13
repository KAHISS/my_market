from django.contrib import admin
from .models import Provider

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'phone')
    search_fields = ('name', 'cnpj')