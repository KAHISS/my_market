# # users/views.py

from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register_view(request):
    """
    Exibe e processa o formulário de registro de novos usuários
    """
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inventory:index')
        else:
            form = AuthenticationForm()
        
        return render(request, 'users/login.html', {'form':form})
    
def logout_view(request):
    """
    Realiza o logout do usuário.
    """
    logout(request)
    return redirect('users:login')