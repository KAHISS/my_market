from django.shortcuts import render
from inventory.models import Product
from utils.pagination import make_pagination
from django.contrib.auth.decorators import login_required

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def pdv(request):
    products = Product.objects.all()

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'sale/pages/pdv.html', {'products': page_obj, 'pagination_range': pagination_range})


@login_required(login_url='users:login', redirect_field_name='next')
def pdv_search(request):
    search_term = request.GET.get('q', '').strip()
    products = Product.objects.filter(name__icontains=search_term)

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'sale/pages/pdv.html', {
        'products': page_obj,
        'pagination_range': pagination_range,
        'search_term': search_term
    })
