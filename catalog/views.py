from inventory.models import Product, Category
from django.shortcuts import get_list_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os
from utils.picture import get_client_picture

PER_PAGE = int(os.environ.get('PER_PAGE', 12))


def catalog(request):
    products = Product.objects.filter(
        in_catalog=True
    ).order_by("name")

    categories = Category.objects.all().order_by("name")

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'catalog/pages/catalogo.html', context={
        'products': page_obj,
        'categories': categories,
        'pagination_range': pagination_range,
        'client_picture': get_client_picture(request.user)
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404("Não encontrado")

    products = Product.objects.filter(
        Q(Q(name__icontains=search_term) | Q(brand__icontains=search_term)) &
        Q(in_catalog=True)
    ).order_by("name")

    categories = Category.objects.all().order_by("name")

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'catalog/pages/search.html', context={
        'page_title': f'Busca por "{search_term}"',
        'search_term': search_term,
        'products': page_obj,
        'categories': categories,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
        'page': f'Busca por "{search_term}"',
        'client_picture': get_client_picture(request.user)
    })


def category(request, category_id):
    products = Product.objects.filter(
        in_catalog=True,
        category_id=category_id
    ).order_by("name")

    categories = Category.objects.all().order_by("name")
    category_name = Category.objects.get(id=category_id).name

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'catalog/pages/category.html', context={
        'products': page_obj,
        'categories': categories,
        'category_name': category_name,
        'pagination_range': pagination_range,
        'page': f'Produtos da categoria {category_name}',
        'client_picture': get_client_picture(request.user)
    })


def offer(request):
    products = Product.objects.filter(
        discount__gt=0,
        in_catalog=True
    ).order_by("name")

    categories = Category.objects.all().order_by("name")

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'catalog/pages/offer.html', context={
        'products': page_obj,
        'categories': categories,
        'pagination_range': pagination_range,
        'page': 'Ofertas em destaque',
        'client_picture': get_client_picture(request.user)
    })


def product(request, product_id):
    item = get_list_or_404(
        Product.objects.filter(
            id=product_id,
            in_catalog=True
        )
    )

    categories = Category.objects.all().order_by("name")

    return render(request, 'catalog/pages/product.html', context={
        'product': item[0],
        'categories': categories,
        'client_picture': get_client_picture(request.user)
    })


def profile(request):
    return render(request, 'catalog/pages/client_profile.html')


def cart(request):
    return render(request, 'catalog/pages/cart.html')
