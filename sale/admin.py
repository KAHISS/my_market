from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Sale, SaleItem


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


class SaleAdmin(admin.ModelAdmin):
    list_display = ('seller', 'total_price', 'discount',
                    'total_quantity', 'created_at', 'updated_at')
    search_fields = ('seller', 'status')
    list_filter = ('created_at', 'updated_at', 'status', 'seller')


class SaleItemsAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'subtotal')
    search_fields = ('sale', 'product', 'quantity', 'subtotal')
    list_filter = ('sale', 'product', 'quantity', 'subtotal')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemsAdmin)
