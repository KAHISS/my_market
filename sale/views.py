from django.shortcuts import render
from .models import CartItem, Cart
from inventory.models import Product
from django.contrib import messages
from django.shortcuts import get_list_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os
from django.shortcuts import redirect


@login_required(login_url='users:login', redirect_field_name='next')
def cart_view(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    if not cart:
        raise Http404('Cart not found')
    return render(request, 'sale/pages/cart.html', {'cart': cart})


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_cart(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(id=id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if cart_item.quantity < product.stock.quantity:
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f'"{product.name}" adicionado ao carrinho.')
    else:
        messages.error(
            request, f'Não há estoque suficiente para adicionar mais um "{product.name}".')

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
                print(cart_item.quantity)
                cart_item.quantity += cart_item.product.unit_per_packaging
                cart_item.save()
        case 'plus':
            if cart_item.quantity < cart_item.product.stock.quantity:
                cart_item.quantity += 1
                cart_item.save()
        case 'minus_packaging':
            if cart_item.quantity >= cart_item.product.unit_per_packaging:
                cart_item.quantity -= cart_item.product.unit_per_packaging
                cart_item.save()
                if cart_item.quantity == 0:
                    cart_item.delete()
        case 'minus':
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                cart_item.save()
                if cart_item.quantity == 0:
                    cart_item.delete()

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
