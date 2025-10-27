from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)
    return render(request, 'users/pages/register.html', {
        'form': form,
        'action': 'Enviar',
        'form_action': reversed('users:register_create')
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
    return render(request, 'users/pages/login.html', {'action': 'Entrar'})


def login_create(request):
    return render(request, 'users/pages/login.html', {'action': 'Entrar'})
