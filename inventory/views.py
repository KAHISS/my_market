from django.shortcuts import render, get_list_or_404
from .models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'global/pages/breve.html')


@login_required(login_url='users:login', redirect_field_name='next')
def product_list(request):
    query = Product.objects.all()

    products = [
        {
            "name": product.name,
            "description": product.description,
            "image": product.image.url if product.image else None,
            "stock": {
                "quantity": product.stock.quantity if getattr(product, 'stock', None) else None,
                "unit": product.stock.sale_price if getattr(product, 'stock', None) else None
            }
        }
        for product in query
    ]

    return JsonResponse({"products": products})
