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
from my_market.settings import STATIC_URL
from django.middleware.csrf import get_token
from utils.pagination import make_pagination
from django.db.models import Q, Sum
import json

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def sale_detail(request, id):
    sale = get_object_or_404(Sale, id=id)
    search_term = request.GET.get('q', '').strip()

    if search_term == 'empty':
        products = []
    else:
        products = Product.objects.filter(
            Q(name__icontains=search_term) |
            Q(barcode__icontains=search_term)
        ).order_by('name')

    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    js_context = {
        "csrf_token": get_token(request),
        "urls": {
            "pdv_search_url": reverse('sale:sale_search', args=[id]),
            "script_message": STATIC_URL
        }
    }

    return render(request, 'sale/pages/sale.html', {
        'sale': sale,
        'products': page_obj,
        'search_term': search_term,
        'pagination_range': pagination_range,
        'js_context': js_context
    })


@login_required(login_url='users:login', redirect_field_name='next')
def sale_search(request, id):
    sale = get_object_or_404(Sale, id=id)
    page_obj, pagination_range = make_pagination(request, products, PER_PAGE)

    return render(request, 'sale/pages/sale.html', {
        'sale': sale,
        'products': page_obj,
        'pagination_range': pagination_range,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def sale_list(request):
    if request.user.is_staff or request.user.is_superuser:
        sales = Sale.objects.all().order_by('-created_at')
    else:
        return redirect('catalog:home')

    stats = {
        'total_orders': sales.count(),
        'total_sales': sales.aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'total_orders_pending': sales.filter(status='pendente').count(),
        'total_sales_pending': sales.filter(status='pendente').aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'total_orders_completed': sales.filter(status='pago').count(),
        'total_sales_completed': sales.filter(status='pago').aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'total_orders_cancelled': sales.filter(status='cancelado').count(),
        'total_sales_cancelled': sales.filter(status='cancelado').aggregate(Sum('total_price'))['total_price__sum'] or 0,
    }

    page_obj, pagination_range = make_pagination(request, sales, PER_PAGE)

    return render(request, 'sale/pages/pdv.html', {
        'sales': page_obj,
        'stats': stats,
        'pagination_range': pagination_range,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_sale(request):
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
        sale_item.get_subtotal()
        sale_item.get_discount()
        sale_item.save()

    if sale_item.discount > 0:
        return JsonResponse({
            'success': True,
            'add_discount': True,
            'created': True if created else False,
            'info_cart_item': {
                'barcode': sale_item.product.barcode,
                'quantity': sale_item.quantity,
                'subtotal': sale_item.subtotal,
                'discount': sale_item.discount,
                'percentage_discount': sale_item.get_percentage_discount(),
                'total_price_with_discount': sale_item.total_price
            },
            'info_cart': {
                'quantity': sale.total_quantity,
                'price': sale.price,
                'total_discount': sale.total_discount,
                'total_price': sale.total_price
            }
        })
    return JsonResponse({
        'success': True,
        'add_discount':  False,
        'created': True if created else False,
        'info_cart_item': {
            'barcode': sale_item.product.barcode,
            'quantity': sale_item.quantity,
            'subtotal': sale_item.subtotal,
            'discount': sale_item.discount,
            'percentage_discount': sale_item.get_percentage_discount(),
            'total_price_with_discount': sale_item.total_price
        },
        'info_cart': {
            'quantity': sale.total_quantity,
            'price': sale.price,
            'total_discount': sale.total_discount,
            'total_price': sale.total_price
        }
    })
