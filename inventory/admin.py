from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Product, Category, Stock, ProductPrintTag


@admin.action(description='Imprimir Etiquetas Selecionadas')
def imprimir_etiquetas(modeladmin, request, queryset):
    # 'queryset' contém todos os produtos que você selecionou ou filtrou
    return render(request, 'inventory/admin/name_tag.html', {'products': queryset})


@admin.action(description='Adicionar Produtos à Impressão')
def add_product_to_print(modeladmin, request, queryset):

    for product in queryset:
        ProductPrintTag.objects.get_or_create(product=product)

    return redirect(request.path)


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
    actions = [add_product_to_print]


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


class ProductPrintTagAdmin(admin.ModelAdmin):
    list_display = ['product', 'resume_name', 'use_resume_name']
    search_fields = 'product__name', 'product__barcode', 'product__category__name'
    list_filter = 'product__category', 'use_resume_name'
    list_editable = ['use_resume_name']
    list_per_page = 10
    actions = [imprimir_etiquetas]


# Register models with their respective admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(ProductPrintTag, ProductPrintTagAdmin)
