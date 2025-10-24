from django.shortcuts import render


def home(request):
    return render(request, 'global/pages/breve.html')
