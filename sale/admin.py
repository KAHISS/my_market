from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'total_discount',
                    'total_quantity', 'created_at', 'updated_at')
    search_fields = ('user',)
    list_filter = ('created_at', 'updated_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal', 'discount',
                    'created_at', 'updated_at')
    search_fields = ('cart', 'product',)
    list_filter = ('created_at', 'updated_at')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'total_discount',
                    'total_quantity', 'created_at', 'updated_at')
    search_fields = ('user',)
    list_filter = ('created_at', 'updated_at')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal', 'discount',
                    'created_at', 'updated_at')
    search_fields = ('order', 'product',)
    list_filter = ('created_at', 'updated_at')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
