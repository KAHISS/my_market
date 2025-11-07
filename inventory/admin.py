from django.contrib import admin
from .models import Product, Category, Stock


class CategoryAdmin(admin.ModelAdmin):
    """
        Admin for Category model.
    """
    ...


class ProductAdmin(admin.ModelAdmin):
    """
        Admin for Product model.
    """
    list_display = ['id', 'name', 'brand', 'category',
                    'sale_price', 'stock_quantity', 'in_catalog']
    list_display_links = 'name', 'brand', 'category', 'sale_price', 'stock_quantity'
    search_fields = 'name', 'brand', 'category__name', 'sale_price', 'stock_quantity'
    list_filter = 'category', 'in_catalog', 'brand'
    list_per_page = 10
    list_editable = ['in_catalog']
    ordering = '-id',
    prepopulated_fields = {'slug': ('name',)}


class StockAdmin(admin.ModelAdmin):
    """
    Admin for Stock model.
    """
    list_display = ['product', 'quantity', 'created_at', 'updated_at']
    list_display_links = 'product', 'quantity', 'created_at', 'updated_at'
    search_fields = 'product__name', 'quantity', 'product__brand', 'product__category__name'
    list_filter = 'product__category', 'product__in_catalog'
    list_per_page = 10
    ordering = '-created_at',


# Register models with their respective admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)
