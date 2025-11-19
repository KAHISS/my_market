from django.shortcuts import render
from .models import CartItem, Cart, Order, OrderItem
from inventory.models import Product
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os
from django.shortcuts import redirect
from client.models import Client
from django.db.models import Sum


@login_required(login_url='users:login', redirect_field_name='next')
def cart_view(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    clients = Client.objects.all()
    if not cart:
        raise Http404('Cart not found')
    return render(request, 'sale/pages/cart.html', {'cart': cart, 'clients': clients})


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_cart(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    cart = Cart.objects.get_or_create(user=request.user)[0]
    product = get_object_or_404(Product, id=id)

    if getattr(product, 'stock', None) is None:
        messages.error(
            request, f'O produto "{product.name}" não tem estoque.')
        return redirect(request.META.get('HTTP_REFERER', 'sale:cart'))

    if product.stock.quantity <= 0:
        messages.error(
            request, f'Não há estoque suficiente para adicionar mais um "{product.name}".')
        return redirect(request.META.get('HTTP_REFERER', 'sale:cart'))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if created:
        cart_item.quantity = 1
    elif cart_item.quantity < product.stock.quantity:
        cart_item.quantity += 1
    else:
        messages.error(
            request, f'Não há estoque suficiente para adicionar mais um "{product.name}".')
        return redirect(request.META.get('HTTP_REFERER', 'sale:cart'))

    cart_item.save()
    messages.success(request, f'{product.name} adicionado ao carrinho.')
    return redirect(request.META.get('HTTP_REFERER', 'sale:cart'))


@login_required(login_url='users:login', redirect_field_name='next')
def update_quantity(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    cart_item = CartItem.objects.get(id=id)
    action = request.POST.get('action')

    match action:
        case 'plus_packaging':
            if (cart_item.quantity + cart_item.product.unit_per_packaging) <= cart_item.product.stock.quantity:
                cart_item.quantity += cart_item.product.unit_per_packaging
                cart_item.save()
            else:
                messages.error(
                    request, f'Não há estoque suficiente para adicionar mais {cart_item.product.packaging_type.lower()} de "{cart_item.product.name}".')
        case 'plus':
            if cart_item.quantity < cart_item.product.stock.quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.error(
                    request, f'Não há estoque suficiente para adicionar mais "{cart_item.product.name}".')
        case 'minus_packaging':
            if cart_item.quantity >= cart_item.product.unit_per_packaging:
                cart_item.quantity -= cart_item.product.unit_per_packaging
                cart_item.save()
        case 'minus':
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                cart_item.save()

    return redirect('sale:cart')


@login_required(login_url='users:login', redirect_field_name='next')
def remove_item(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()

    messages.success(
        request, f'{cart_item.product.name} removido do carrinho.')
    return redirect('sale:cart')


@login_required(login_url='users:login', redirect_field_name='next')
def checkout(request):
    if not request.POST:
        raise Http404("No POST data found.")

    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()

    if cart_items.count() == 0:
        messages.warning(request, 'Não há itens no carrinho.')
        return redirect('sale:cart')

    for item in cart_items:
        if item.quantity > item.product.stock.quantity:
            messages.error(
                request, f'Não há estoque suficiente para "{item.product.name}".')
            return redirect('sale:cart')

        item.product.stock.quantity -= item.quantity
        item.product.stock.save()

    client = None
    seller = None
    if request.user.is_staff or request.user.is_superuser:
        client_id = request.POST.get('client')
        client = Client.objects.get(id=client_id).user
        seller = request.user
    else:
        client = request.user
        seller = None

    new_order = Order.objects.create(
        user=client,
        seller=seller,
        status='pendente',
        total_price=cart.total_price(),
        total_discount=cart.total_discount(),
        total_quantity=cart.total_quantity(),
        total_price_with_discount=cart.total_price_with_discount(),
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            subtotal=item.subtotal(),
            percentage_discount=item.percentage_discount(),
            discount=item.discount(),
            total_price_with_discount=item.total_price_with_discount(),
        )

    cart_items.delete()

    messages.success(request, 'Compra realizada com sucesso.')

    return redirect('sale:order', id=new_order.id)


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
