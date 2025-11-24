import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Sum, Q
from django.db import transaction
from sale.models import Order
from client.models import Client
from inventory.models import Product
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 12))


@login_required(login_url='users:login', redirect_field_name='next')
def order_list(request):
    if request.user.is_staff or request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(
            user=request.user).order_by('-created_at')

    stats = {
        'total_orders': orders.count(),
        'total_sales': orders.aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_pending': orders.filter(status='pendente').count(),
        'total_sales_pending': orders.filter(status='pendente').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_completed': orders.filter(status='pago').count(),
        'total_sales_completed': orders.filter(status='pago').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_cancelled': orders.filter(status='cancelado').count(),
        'total_sales_cancelled': orders.filter(status='cancelado').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
    }

    page_obj, pagination_range = make_pagination(request, orders, PER_PAGE)

    return render(request, 'sale/pages/orders.html', {
        'orders': page_obj,
        'stats': stats,
        'pagination_range': pagination_range,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def search_order(request):
    search_term = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    search_date = request.GET.get('date', '')

    if request.user.is_staff or request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    if search_term:
        text_query = Q(
            Q(user__username__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(seller__username__icontains=search_term) |
            Q(seller__first_name__icontains=search_term) |
            Q(seller__last_name__icontains=search_term)
        )

        if search_term.isdigit():
            text_query |= Q(id=int(search_term))

        orders = orders.filter(text_query)

    # 5. Lógica de Filtro por Data (Separado para evitar erros de formato)
    if search_date:
        # O lookup __date compara ignorando as horas
        orders = orders.filter(created_at__date=search_date)

    # 6. Lógica de Filtro por Status
    if status:
        orders = orders.filter(status=status)

    # Ordenação final
    # Geralmente decrescente é melhor para ver os novos
    orders = orders.order_by("-created_at")

    # Estatísticas (Mantive sua lógica, apenas indentada)
    stats = {
        'total_orders': orders.count(),
        'total_sales': orders.aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_pending': orders.filter(status='pendente').count(),
        'total_sales_pending': orders.filter(status='pendente').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_completed': orders.filter(status='pago').count(),
        'total_sales_completed': orders.filter(status='pago').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_cancelled': orders.filter(status='cancelado').count(),
        'total_sales_cancelled': orders.filter(status='cancelado').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
    }

    page_obj, pagination_range = make_pagination(request, orders, PER_PAGE)

    # Monta a string de query adicional para a paginação não perder os filtros
    additional_url_query = f'&q={search_term}&status={status}&date={search_date}'

    return render(request, 'sale/pages/orders.html', context={
        'page_title': f'Busca Avançada',  # Mudei o título pois pode não ter search_term
        'search_term': search_term,
        'search_date': search_date,  # Passar para o template para manter o input preenchido
        'orders': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': additional_url_query,
        'stats': stats,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def order_detail(request, id):
    order = Order.objects.get(id=id)
    client = Client.objects.get(user=order.user)

    if order.user != request.user and not request.user.is_staff and not request.user.is_superuser:
        raise Http404("Order not found.")

    return render(request, 'sale/pages/order_detail.html', {
        'order': order,
        'client': client,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def order_cancel(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404("Order not found.")

    order = Order.objects.get(id=id)

    if order.status == 'cancelado':
        messages.info(request, 'Este pedido já foi cancelado.')
        return redirect('sale:order_detail', id=order.id)

    order_items = order.order_items.all()

    try:
        # INÍCIO DA TRANSAÇÃO (Tudo ou Nada)
        with transaction.atomic():

            # 1. Validação de Estoque e Dedução
            for item in order_items:
                # CRÍTICO: select_for_update() trava este produto para escrita.
                # Usamos select_related('stock') se o estoque for uma tabela separada (OneToOne)
                # get(id=...) garante que estamos indo no banco buscar a versão mais atual
                product_db = Product.objects.select_for_update(
                ).select_related('stock').get(id=item.product.id)

                # Deduz o estoque
                product_db.stock.quantity += item.quantity
                product_db.stock.save()

        order.status = 'cancelado'
        order.save()

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('sale:order_detail', id=order.id)

    messages.success(request, 'Pedido cancelado com sucesso.')
    return redirect('sale:order_detail', id=order.id)
