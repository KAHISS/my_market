from django.contrib import admin
from django.shortcuts import render
from .models import Product, Category, Stock


@admin.action(description='Imprimir Etiquetas Selecionadas')
def imprimir_etiquetas(modeladmin, request, queryset):
    # 'queryset' contém todos os produtos que você selecionou ou filtrou
    return render(request, 'inventory/admin/name_tag.html', {'products': queryset})


class CategoryAdmin(admin.ModelAdmin):
    """
        Admin for Category model.
    """
    ...


class ProductAdmin(admin.ModelAdmin):
    """
        Admin for Product model.
    """
    list_display = ['id', 'name', 'brand', 'category', 'in_catalog']
    list_display_links = 'name', 'brand', 'category'
    search_fields = 'name', 'brand', 'category__name', 'barcode'
    list_filter = 'category', 'in_catalog', 'brand'
    list_per_page = 10
    list_editable = ['in_catalog']
    ordering = '-id',
    prepopulated_fields = {'slug': ('name',)}
    actions = [imprimir_etiquetas]


class StockAdmin(admin.ModelAdmin):
    """
    Admin for Stock model.
    """
    list_display = ['product', 'quantity', 'created_at', 'updated_at']
    list_display_links = 'product', 'quantity', 'created_at', 'updated_at'
    search_fields = 'product__name', 'quantity', 'product__brand', 'product__category__name', 'product__barcode'
    list_filter = 'product__category', 'product__in_catalog'
    list_per_page = 10
    ordering = '-created_at',


# Register models with their respective admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)
