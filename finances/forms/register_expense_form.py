from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from finances.models import Expense, Kind


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'kind', 'amount', 'modality', 'payment_method',
            'status', 'pay_by', 'payday', 'observation', 'proof'
        ]
        labels = {
            'kind': 'Tipo da despesa',
            'amount': 'Valor (R$)',
            'modality': 'Modalidade de Compra',
            'payment_method': 'Forma de Pagamento',
            'status': 'Status Atual',
            'pay_by': 'Data de Vencimento',
            'payday': 'Data do Pagamento',
            'observation': 'Observações Adicionais',
            'proof': 'Comprovante (Foto ou PDF)'
        }
        widgets = {
            'pay_by': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'payday': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'amount': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Valor'}),
            'observation': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observação'}),
            'proof': forms.FileInput(attrs={'placeholder': 'Comprovante'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Div('kind', css_class='w-full'),
                Div('amount', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'
            ),
            Div(
                Div('modality', css_class='w-full'),
                Div('payment_method', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'
            ),
            Div(
                Div('status', css_class='w-full'),
                Div('pay_by', css_class='w-full'),
                Div('payday', css_class='w-full'),
                css_class='grid grid-cols-1 md:grid-cols-3 gap-4 mb-4'
            ),
            Div(
                'observation',
                css_class='mb-4'
            ),
            Div(
                'proof',
                css_class='mb-4'
            )
        )
