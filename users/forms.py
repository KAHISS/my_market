# users/forms.py
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterFrom(UserCreationForm):
    """
    Formulário para registrar um novo usuário.
    """
    email = forms.EmailField(label="E-mail")

    class Meta: 
        model = User
        fields = ["username", "email", "first_name", "last_name"]

