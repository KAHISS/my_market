from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from client.models import Client

# Create your views here.


@login_required(login_url='users:login', redirect_field_name='next')
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
        # save the new user
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        # create a client for the new user
        Client.objects.create(user=user)
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
    return redirect(reverse('catalog:home'))


@login_required(login_url='users:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        raise Http404("No POST data found.")

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('users:login'))

    logout(request)
    return redirect(reverse('users:login'))
