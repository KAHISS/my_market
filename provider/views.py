from django.shortcuts import render

def index(request):
    return render(request, 'provider/pages/index.html')
