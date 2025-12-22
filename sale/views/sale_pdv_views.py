from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from sale.models import Sale, SaleItem
from inventory.models import Product
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from client.models import Client
from my_market.settings import STATIC_URL
from django.middleware.csrf import get_token
from utils.pagination import make_pagination
from django.db.models import Q
import json

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def sale(request):
    products = Product.objects.all().order_by('name')

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    js_context = {
        "csrf_token": get_token(request),
        "urls": {
            "pdv_search_url": reverse('sale:sale_search'),
            "script_message": STATIC_URL
        }
    }

    return render(request, 'sale/pages/sale.html', {
        'products': page_obj,
        'pagination_range': pagination_range,
        'js_context': js_context
    })


@login_required(login_url='users:login', redirect_field_name='next')
def sale_search(request):
    search_term = request.GET.get('q', '').strip()
    products = Product.objects.filter(
        Q(name__icontains=search_term) |
        Q(barcode__icontains=search_term)
    ).order_by('name')

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    js_context = {
        "csrf_token": get_token(request),
        "urls": {
            "pdv_search_url": reverse('sale:sale_search'),
            "script_message": STATIC_URL
        }
    }

    return render(request, 'sale/pages/sale.html', {
        'products': page_obj,
        'pagination_range': pagination_range,
        'search_term': search_term,
        'js_context': js_context
    })


@login_required(login_url='users:login', redirect_field_name='next')
def sales_list(request):
    return render(request, 'sale/pages/pdv.html')


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_cart_pdv(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Erro no formato dos dados enviados.'})

    barcode = data.get('barcode')
    quantity = data.get('quantity')
    sale_id = data.get('sale_id')

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Quantidade inválida.'})

    if not barcode or quantity < 1 or not sale_id:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    sale = Sale.objects.get_or_create(id=sale_id)[0]

    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(), barcode__icontains=barcode)

        if getattr(product, 'stock', None) is None:
            return JsonResponse({'success': False, 'message': 'Erro de cadastro: produto sem estoque vinculado.'})

        if product.stock.quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Estoque esgotado.'})

        sale_item, created = SaleItem.objects.get_or_create(
            sale=sale,
            product=product,
            defaults={'quantity': 0}
        )

        if created and sale_item.quantity != 0:
            sale_item.quantity = 0

        final_quantity = sale_item.quantity + quantity

        if final_quantity > product.stock.quantity:
            msg = f'Estoque insuficiente. Você já tem {sale_item.quantity} no carrinho e só restam {product.stock.quantity} no total.'
            return JsonResponse({'success': False, 'message': msg})

        sale_item.quantity += quantity
        sale_item.save()

    if sale_item.discount > 0:
        return JsonResponse({
            'success': True,
            'add_discount': True,
            'info_cart_item': {
                'quantity': sale_item.quantity,
                'subtotal': sale_item.subtotal,
                'discount': sale_item.discount,
                'percentage_discount': sale_item.get_percentage_discount(),
                'total_price_with_discount': sale_item.total_price
            },
            'info_cart': {
                'quantity': sale.quantity,
                'total_price': sale.total_price,
                'total_discount': sale.total_discount,
                'total_price_with_discount': sale.total_price
            }
        })
    return JsonResponse({
        'success': True,
        'add_discount':  False,
        'info_cart_item': {
            'quantity': sale_item.quantity,
            'subtotal': sale_item.subtotal,
            'discount': sale_item.discount,
            'percentage_discount': sale_item.get_percentage_discount(),
            'total_price_with_discount': sale_item.total_price
        },
        'info_cart': {
            'quantity': sale.quantity,
            'total_price': sale.total_price,
            'total_discount': sale.total_discount,
            'total_price_with_discount': sale.total_price
        }
    })
