from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user',)
    list_filter = ('created_at', 'updated_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity',
                    'created_at', 'updated_at')
    search_fields = ('cart', 'product',)
    list_filter = ('created_at', 'updated_at')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
