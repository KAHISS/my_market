from django.shortcuts import render
from inventory.models import Product
from utils.pagination import make_pagination


def pdv(request):
    products = Product.objects.all()

    page_obj, pagination_range = make_pagination(request, products, 1)

    return render(request, 'sale/pages/pdv.html', {'products': page_obj, 'pagination_range': pagination_range})
