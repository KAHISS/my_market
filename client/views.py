from django.shortcuts import render
from .models import Client

# Create your views here.
def profile(request):
    return render(request, 'client/pages/profile.html')

def profile(request, id): 
    client = Client.objects.filter(id=id).first()
    return render(request, 'client/pages/profile.html', context= {
                'client': client})

def management(request):
    clients = Client.objects.all()
    return render(request, 'client/pages/clients-management.html', context={
        'clients': clients})

def add_client(request):
    return render(request, 'client/pages/add-new-client.html')