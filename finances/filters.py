import django_filters
from django import forms
from .models import Expense, Kind


class ExpenseFilter(django_filters.FilterSet):
    # Filtro de período para Data de Vencimento
    pay_by = django_filters.DateFromToRangeFilter(
        field_name='pay_by',
        label='Vencimento (Início/Fim)',
        widget=django_filters.widgets.DateRangeWidget(attrs={
            'type': 'date',
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
        })
    )

    # Filtro de período para Data de Pagamento
    payday = django_filters.DateFromToRangeFilter(
        field_name='payday',
        label='Pagamento (Início/Fim)',
        widget=django_filters.widgets.DateRangeWidget(attrs={
            'type': 'date',
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
        })
    )

    modality = django_filters.ChoiceFilter(
        choices=Expense.Modality.choices,
        label='Modalidade'
    )

    kind = django_filters.ModelChoiceFilter(
        queryset=Kind.objects.all(),
        label="Categoria da Despesa",  # O novo nome que aparecerá no formulário
    )

    payment_method = django_filters.ChoiceFilter(
        choices=Expense.PaymentMethod.choices,
        label='Método de Pagamento'
    )

    class Meta:
        model = Expense
        fields = ['modality', 'kind', 'status', 'payment_method']
