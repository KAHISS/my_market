from django.contrib import admin
from .models import Expense, Kind

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'modality', 'kind', 'pay_by', 'payday',
        'amount', 'status', 'payment_method', 'created_at'
    )
    list_filter = ('modality', 'status', 'payment_method', 'kind')
    search_fields = ('user__username', 'kind__name', 'observation')
    ordering = ('-created_at',)


class KindAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Kind, KindAdmin)
