from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.


def register(request):
    form = RegisterForm()
    return render(request, 'users/pages/register_view.html', {'form': form})
