from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from .models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'inventory/pages/storage.html', context={
        'products': products}
    )


def product(request, id):
    product = get_list_or_404(
        Product.objects.filter(
            id=id
        )
    )
    return render(request, 'inventory/pages/product-view.html', context={
        'product': product[0],
        'title': f"Produto - {product[0].name}"
    }
    )


def addProduct(request):
    return render(request, 'inventory/pages/addNewProduct-view.html')
