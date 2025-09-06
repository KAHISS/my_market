from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'inventory/pages/storage.html', context={
        'products': products}
    )


def product(request, id):
    product = Product.objects.filter(id=id).first()
    return render(request, 'inventory/pages/product-view.html', context={
        'product': product}
    )


def addProduct(request):
    return render(request, 'inventory/pages/addNewProduct-view.html')
