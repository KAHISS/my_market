from datetime import timedelta
from django.utils import timezone
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
from decimal import Decimal
import json
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 12))


@login_required(login_url='users:login', redirect_field_name='next')
def create_new_sale(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    sale = Sale.objects.create(seller=request.user)

    # Exemplo de comando de limpeza
    Sale.objects.filter(
        sale_items__isnull=True,
        status='pendente'
    ).exclude(
        id=sale.id
    ).delete()

    return redirect('sale:sale_detail', id=sale.id)


@login_required(login_url='users:login', redirect_field_name='next')
def sale_detail(request, id):
    sale = get_object_or_404(Sale, id=id)
    sale_items = sale.sale_items.all()
    search_term = request.GET.get('q', 'empty').strip()

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
            "remove_item_url": reverse('sale:sale_remove')
        }
    }

    return render(request, 'sale/pages/sale.html', {
        'sale': sale,
        'items': sale.sale_items.all(),
        'products': page_obj,
        'search_term': search_term,
        'pagination_range': pagination_range,
        'js_context': js_context
    })


@login_required(login_url='users:login', redirect_field_name='next')
def sale_search(request, id):
    sale = get_object_or_404(Sale, id=id)
    sale_items = sale.sale_items.all()
    page_obj, pagination_range = make_pagination(request, sale_items, PER_PAGE)

    return render(request, 'sale/pages/sale.html', {
        'sale': sale,
        'sale_items': sale.sale_items.all(),
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
def search_sales(request):
    search_term = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    search_date = request.GET.get('date', '')

    if request.user.is_staff or request.user.is_superuser:
        sales = Sale.objects.all()
    else:
        sales = Sale.objects.filter(user=request.user)

    if search_term:
        text_query = Q(
            Q(client__icontains=search_term) |
            Q(seller__username__icontains=search_term) |
            Q(seller__first_name__icontains=search_term) |
            Q(seller__last_name__icontains=search_term)
        )

        if search_term.isdigit():
            text_query |= Q(id=int(search_term))

        sales = sales.filter(text_query)

    # 5. Lógica de Filtro por Data (Separado para evitar erros de formato)
    if search_date:
        # O lookup __date compara ignorando as horas
        sales = sales.filter(created_at__date=search_date)

    # 6. Lógica de Filtro por Status
    if status:
        sales = sales.filter(status=status)

    # Ordenação final
    # Geralmente decrescente é melhor para ver os novos
    sales = sales.order_by("-created_at")

    # Estatísticas (Mantive sua lógica, apenas indentada)
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

    # Monta a string de query adicional para a paginação não perder os filtros
    additional_url_query = f'&q={search_term}&status={status}&date={search_date}'

    return render(request, 'sale/pages/pdv.html', context={
        'page_title': f'Busca Avançada',  # Mudei o título pois pode não ter search_term
        'search_term': search_term,
        'search_date': search_date,  # Passar para o template para manter o input preenchido
        'sales': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': additional_url_query,
        'stats': stats,
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

    if not barcode or quantity is None or not sale_id:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    sale = Sale.objects.get_or_create(id=sale_id)[0]

    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(), barcode__icontains=barcode)

        if getattr(product, 'stock', None) is None:
            return JsonResponse({'success': False, 'message': 'Erro de cadastro: produto sem estoque vinculado.'})

        sale_item, created = SaleItem.objects.get_or_create(
            sale=sale,
            product=product,
            defaults={'quantity': 0}
        )

        if created and sale_item.quantity != 0:
            sale_item.quantity = 0

        '''if product.stock.quantity - quantity < 0:
            msg = f'Estoque insuficiente. Só restam {product.stock.quantity} no estoque.'
            if created:
                sale_item.delete()
            return JsonResponse({'success': False, 'message': msg})'''

        product.stock.quantity -= quantity
        if product.stock.quantity <= 0:
            product.stock.quantity = 0
        product.stock.save()

        sale_item.quantity += quantity

        if sale_item.quantity == 0:
            item_id = sale_item.id
            sale_item.delete()
            sale.get_total_quantity()
            sale.get_subtotal()
            sale.get_total_price()
            return JsonResponse({
                'success': True,
                'message': 'Produto adicionado ao carrinho com sucesso.' if quantity > 0 else 'Produto removido do carrinho com sucesso.',
                'item': {
                    'id': item_id,
                    'remove': True
                },
                'sale': {
                    'id': sale.id,
                    'client': sale.client,
                    'quantity': sale.total_quantity,
                    'subtotal': sale.subtotal,
                    'discount': sale.discount,
                    'freight': sale.freight,
                    'total_price': sale.total_price
                }
            })
        else:
            sale_item.get_subtotal()
            sale_item.save()

        sale.get_total_quantity()
        sale.get_subtotal()
        sale.get_total_price()

    return JsonResponse({
        'success': True,
        'add_discount':  False,
        'message': 'Produto adicionado ao carrinho com sucesso.' if quantity > 0 else 'Produto removido do carrinho com sucesso.',
        'created': True if created else False,
        'item': {
            'id': sale_item.id,
            'barcode': sale_item.product.barcode,
            'name': sale_item.product.name,
            'quantity': sale_item.quantity,
            'subtotal': sale_item.subtotal,
            'url_remove': reverse('sale:sale_remove'),
        },
        'sale': {
            'id': sale.id,
            'client': sale.client,
            'quantity': sale.total_quantity,
            'subtotal': sale.subtotal,
            'discount': sale.discount,
            'freight': sale.freight,
            'total_price': sale.total_price
        }
    })


@login_required(login_url='users:login', redirect_field_name='next')
def update_sale_summary(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Erro no formato dos dados enviados.'})

    sale_id = data.get('sale_id')
    client = data.get('client')
    discount = data.get('discount')
    freight = data.get('freight')

    try:
        discount = Decimal(discount)
        freight = Decimal(freight)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    if not sale_id or discount < 0 or freight < 0:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    sale = Sale.objects.get(id=sale_id)
    sale.discount = discount
    sale.freight = freight
    sale.client = client
    sale.save()
    sale.get_total_price()
    return JsonResponse({
        'success': True,
        'message': 'Resumo atualizado com sucesso.',
        'sale': {
            'id': sale.id,
            'client': sale.client,
            'quantity': sale.total_quantity,
            'subtotal': sale.subtotal,
            'discount': sale.discount,
            'freight': sale.freight,
            'total_price': sale.total_price
        }
    })


@login_required(login_url='users:login', redirect_field_name='next')
def remove_item_from_sale(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Erro no formato dos dados enviados.'})

    item_id = data.get('item_id')
    sale_id = data.get('sale_id')

    if not item_id or not sale_id:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})
    sale = Sale.objects.get(id=sale_id)
    item = SaleItem.objects.get(id=item_id)

    item.product.stock.quantity += item.quantity
    item.product.stock.save()

    item.delete()
    sale.get_total_quantity()
    sale.get_subtotal()
    sale.get_total_price()
    return JsonResponse({
        'success': True,
        'message': 'Item removido com sucesso.',
        'sale': {
            'id': sale.id,
            'client': sale.client,
            'quantity': sale.total_quantity,
            'subtotal': sale.subtotal,
            'discount': sale.discount,
            'freight': sale.freight,
            'total_price': sale.total_price
        },
        'item': {
            'id': item_id,
            'remove': True
        }
    })


@login_required(login_url='users:login', redirect_field_name='next')
def finish_sale(request, id):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    payment_method = request.POST.get('payment_method')
    value_received = request.POST.get('value_received')
    sale = Sale.objects.get(id=id)
    sale.status = 'pago'
    sale.payment_method = payment_method
    sale.cash_received = value_received
    sale.save()

    return redirect('sale:sale_detail', id=id)


@login_required(login_url='users:login', redirect_field_name='next')
def cancel_sale(request, id):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    sale = Sale.objects.get(id=id)
    sale.status = 'cancelado'
    sale.save()

    sale_items = SaleItem.objects.filter(sale=sale)
    for item in sale_items:
        item.product.stock.quantity += item.quantity
        item.product.stock.save()

    return redirect('sale:sale_list')
