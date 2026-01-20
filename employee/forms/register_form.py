from django import forms
from django.contrib.auth.models import User
from employee.models import Employee  # Ajuste o import conforme seu app
from utils.django_forms import add_placeholder, strong_password


class EmployeeRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionando placeholders para os novos campos
        add_placeholder(self.fields['position'], 'Ex: Gerente de Vendas')
        add_placeholder(self.fields['hire_date'], 'Data de contratação')
        add_placeholder(self.fields['salary'], 'Ex: 2500.00')

    user = forms.Select(
        label='Usuário',
        queryset=User.objects.all(),
        error_messages={'required': 'O usuário é obrigatório.'}
    )

    position = forms.CharField(
        label='Cargo',
        max_length=100,
        error_messages={'required': 'O cargo é obrigatório.'}
    )

    hire_date = forms.DateField(
        label='Data de Contratação',
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': 'A data de contratação é obrigatória.'}
    )

    salary = forms.DecimalField(
        label='Salário',
        max_digits=10,
        decimal_places=2,
        error_messages={'required': 'O salário é obrigatório.'}
    )

    class Meta:
        model = Employee
        fields = ['user', 'position', 'hire_date', 'salary']
        error_class = 'error'
