from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    return render(request, 'users/pages/register.html', {
        'form': form,
        'action': 'Enviar',
        'form_action': reverse('users:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404("No POST data found.")

    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Usuário criado com sucesso!')

        del (request.session["register_form_data"])

    return redirect('users:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'users/pages/login.html', {
        'form': form,
        'action': 'Entrar',
        'form_action': reverse('users:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404("No POST data found.")

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )

        if authenticate_user is not None:
            messages.success(request, 'Login realizado com sucesso!')
            login(request, authenticate_user)

        else:
            messages.error(request, 'Credenciais inválidas!')
    else:
        messages.error(request, 'Erro ao validar formulário!')
    return redirect(reverse('users:login'))
