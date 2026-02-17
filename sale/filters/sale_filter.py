import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from sale.models import Sale


def tailwind_css_classes():
    return 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'


class SaleFilter(django_filters.FilterSet):
    seller = django_filters.CharFilter(
        field_name='seller__username',
        lookup_expr='icontains',
        label='Vendedor',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do vendedor',
            'class': tailwind_css_classes()
        })
    )

    client = django_filters.CharFilter(
        field_name='client',
        lookup_expr='icontains',
        label='Cliente',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome ou CPF do cliente',
            'class': tailwind_css_classes()
        })
    )

    created_at = django_filters.DateFromToRangeFilter(
        field_name='created_at',
        label='Criado em (Início/Fim)',
        widget=django_filters.widgets.DateRangeWidget(attrs={
            'type': 'date',
            'class': tailwind_css_classes()
        })
    )

    updated_at = django_filters.DateFromToRangeFilter(
        field_name='updated_at',
        label='Atualizado em (Início/Fim)',
        widget=django_filters.widgets.DateRangeWidget(attrs={
            'type': 'date',
            'class': tailwind_css_classes()
        })
    )

    modality = django_filters.ChoiceFilter(
        choices=Sale.Modality.choices,
        label='Modalidade',
        widget=forms.Select(attrs={
            'class': tailwind_css_classes()
        })
    )

    status = django_filters.ChoiceFilter(
        choices=Sale.Status.choices,
        label='Status',
        widget=forms.Select(attrs={
            'class': tailwind_css_classes()
        })
    )

    payment_method = django_filters.ChoiceFilter(
        choices=Sale.PaymentMethod.choices,
        label='Método de Pagamento',
        widget=forms.Select(attrs={
            'class': tailwind_css_classes()
        })
    )

    total_price = django_filters.RangeFilter(
        field_name='total_price',
        label='Valor Total (Mín/Máx)',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'number',
            'step': '0.01',
            'class': tailwind_css_classes()
        })
    )

    class Meta:
        model = Sale
        fields = [
            'seller', 'client', 'created_at', 'updated_at',
            'modality', 'status', 'payment_method', 'total_price'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        self.helper.layout = Layout(
            HTML("""
            <details class="bg-white border border-gray-300 rounded-md shadow-sm mb-6 group">
                <summary class="list-none flex flex-wrap items-center cursor-pointer
                                focus-visible:outline-none focus-visible:ring focus-visible:ring-indigo-500
                                rounded group-open:rounded-b-none group-open:z-[1] relative
                                py-2.5 pl-4 pr-3 border-b border-transparent group-open:border-gray-200 hover:bg-gray-50">
                    <h3 class="flex-1 font-semibold text-gray-700">
                        <i class="fas fa-filter mr-2"></i> Filtros de Pesquisa
                    </h3>
                    <div class="flex items-center">
                        <span class="text-gray-500 transform group-open:rotate-180 transition-transform duration-200">
                            ▼
                        </span>
                    </div>
                </summary>
                <div class="p-4">
            """),

            Div(
                Div('seller', css_class='w-full'),
                Div('client', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'
            ),

            Div(
                Div('created_at', css_class='w-full'),
                Div('updated_at', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'
            ),

            Div(
                Div('modality', css_class='w-full'),
                Div('status', css_class='w-full'),
                Div('payment_method', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-3 gap-4 mb-4'
            ),

            Div(
                Div('total_price', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-1 gap-4 mb-4'
            ),

            Div(
                Submit('submit', 'Filtrar',
                       css_class='bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow'),
                HTML('<a href="." class="ml-4 inline-block align-middle text-gray-600 hover:text-gray-800 underline">Limpar Filtros</a>'),
                css_class='flex items-center justify-end mt-4 pt-4 border-t border-gray-100'
            ),

            # --- Fim do Accordion ---
            HTML("""
                </div>
            </details>
            """)
        )
