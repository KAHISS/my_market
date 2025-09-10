from django.shortcuts import render

def index(request):
    return render(request, 'provider/pages/index.html')

def add_provider(request):
    return render(request, 'provider/pages/add_provider.html')