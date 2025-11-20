from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Sum
from sale.models import Order
from client.models import Client


@login_required(login_url='users:login', redirect_field_name='next')
def order_list(request):
    if request.user.is_staff or request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    stats = {
        'total_orders': orders.count(),
        'total_sales': orders.aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_pending': orders.filter(status='pendente').count(),
        'total_sales_pending': orders.filter(status='pendente').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
        'total_orders_completed': orders.filter(status='completo').count(),
        'total_sales_completed': orders.filter(status='completo').aggregate(Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0,
    }

    return render(request, 'sale/pages/orders.html', {
        'orders': orders,
        'stats': stats,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def order_detail(request, id):
    order = Order.objects.get(id=id)
    client = Client.objects.get(user=request.user)

    if order.user != request.user and not request.user.is_staff and not request.user.is_superuser:
        raise Http404("Order not found.")

    return render(request, 'sale/pages/order_detail.html', {
        'order': order,
        'client': client,
    })
