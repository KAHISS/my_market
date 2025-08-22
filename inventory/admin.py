from django.contrib import admin
from .models import Product, StockMovement, Category


class CategoryAdmin(admin.ModelAdmin):
    """
        Admin for Category model.
    """
    ...


class ProductAdmin(admin.ModelAdmin):
    """
        Admin for Product model.
    """
    ...


class StockMovementAdmin(admin.ModelAdmin):
    """
        Admin for StockMovement model.
    """
    ...


# Register models with their respective admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(StockMovement, StockMovementAdmin)
admin.site.register(Category, CategoryAdmin)
