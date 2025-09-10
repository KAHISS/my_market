from django.shortcuts import render

def index_provider(request):
    return render(request, 'provider/pages/provider.html')

def add_provider(request):
    return render(request, 'provider/pages/add_provider.html')