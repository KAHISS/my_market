from django import forms
from django.contrib.auth.models import User
from client.models import Client
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex: João')
        add_placeholder(self.fields['last_name'], 'Ex: Silva')
        add_placeholder(self.fields['username'], 'Ex: joao123')
        add_placeholder(self.fields['email'], 'Ex: joao123@gmail.com')
        add_placeholder(self.fields['password'], 'Ex: João@123')
        add_placeholder(self.fields['password2'], 'Confirme sua senha')

    first_name = forms.CharField(
        label='Primeiro nome',
        error_messages={'required': 'O primeiro nome é obrigatório.'},
    )

    last_name = forms.CharField(
        label='Sobrenome',
        error_messages={'required': 'O sobrenome é obrigatório.'},
    )

    username = forms.CharField(
        label='Nome de usuário',
        help_text=(
            "O usuário deve conter apenas letras, números e @/./+/-/_."
            "O tamanho deve estar entre 4 e 150 caracteres."
        ),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'O tamanho mínimo é 4 caracteres.',
            'max_length': 'O tamanho máximo é 150 caracteres.'
        },
        min_length=4, max_length=150
    )

    email = forms.EmailField(
        label='Endereço de email',
        error_messages={
            'required': 'O e-mail é obrigatório.',
            'invalid': 'Digite um endereço de e-mail válido.'
        }
    )

    # --- Campos de senha que já estavam definidos ---

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        validators=[strong_password],
        error_messages={
            'required': 'A senha é obrigatória.'
        },
        help_text='A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números.',
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A confirmação da senha é obrigatória.'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Esse nome de usuário já está em uso.',
                code='invalid',
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Esse e-mail já está em uso.',
                code='invalid',
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError({
                'password2': forms.ValidationError(
                    'As senhas não coincidem.',
                    code='invalid',
                )
            })
        return cleaned_data
