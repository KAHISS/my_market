from django.shortcuts import render
from inventory.models import Product

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog/pages/catalogo.html', context={
        'products': products})
