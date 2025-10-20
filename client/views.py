from django.shortcuts import render
from .models import Client
from validate_docbr import CNPJ, CPF

# Create your views here.


def profile(request, id):
    client = Client.objects.filter(id=id).first()
    client.cnpj = CNPJ().mask(client.cnpj)
    client.cpf = CPF().mask(client.cpf)
    return render(request, 'client/pages/profile.html', context={
        'client': client})


def management(request):
    clients = Client.objects.all()
    return render(request, 'client/pages/clients-management.html', context={
        'clients': clients})


def add_client(request):
    return render(request, 'client/pages/add-new-client.html')


def edit_client(request, id):
    # Lógica para editar o cliente virá aqui
    # Por enquanto, podemos apenas renderizar um template
    return render(request, 'client/pages/edit-client.html')


def delete_client(request, id):
    # Lógica para editar o cliente virá aqui
    # Por enquanto, podemos apenas renderizar um template
    return render(request, 'client/pages/delete-client.html')
