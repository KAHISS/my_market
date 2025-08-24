from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'inventory/pages/storage.html', context={
        'products': products})
