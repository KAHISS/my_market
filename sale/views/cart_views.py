from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from sale.models import CartItem, Cart
from inventory.models import Product
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from client.models import Client
from my_market.settings import STATIC_URL
from django.middleware.csrf import get_token
import json


@login_required(login_url='users:login', redirect_field_name='next')
def cart_view(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    clients = Client.objects.all()
    if not cart:
        raise Http404('Cart not found')

    if cart.total_discount() > 0:
        display_discount = True
    else:
        display_discount = False

    js_context = {
        "csrf_token": get_token(request),
        "urls": {
            "catalog": reverse('catalog:home'),
            "add_to_cart": reverse('sale:cart_add'),
            "remove_from_cart": reverse('sale:cart_remove'),
            "script_message": STATIC_URL
        }
    }

    return render(request, 'sale/pages/cart.html', {'cart': cart, 'clients': clients, 'js_context': js_context, 'display_discount': display_discount})


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_cart(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Erro no formato dos dados enviados.'})

    productId = data.get('productId')
    quantity = data.get('quantity')

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Quantidade inválida.'})

    if not productId or quantity < 1:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    cart = Cart.objects.get_or_create(user=request.user)[0]

    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(), id=productId)

        if getattr(product, 'stock', None) is None:
            return JsonResponse({'success': False, 'message': 'Erro de cadastro: produto sem estoque vinculado.'})

        if product.stock.quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Estoque esgotado.'})

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )

        if created and cart_item.quantity != 0:
            cart_item.quantity = 0

        final_quantity = cart_item.quantity + quantity

        if final_quantity > product.stock.quantity:
            msg = f'Estoque insuficiente. Você já tem {cart_item.quantity} no carrinho e só restam {product.stock.quantity} no total.'
            return JsonResponse({'success': False, 'message': msg})

        cart_item.quantity += quantity
        cart_item.save()

    if cart_item.discount() > 0:
        return JsonResponse({
            'success': True,
            'message': f'{product.name} adicionado ao carrinho.',
            'add_discount': True,
            'info_cart_item': {
                'quantity': cart_item.quantity,
                'subtotal': cart_item.subtotal(),
                'discount': cart_item.discount(),
                'percentage_discount': cart_item.percentage_discount(),
                'total_price_with_discount': cart_item.total_price_with_discount()
            },
            'info_cart': {
                'quantity': cart.total_quantity(),
                'total_price': cart.total_price(),
                'total_discount': cart.total_discount(),
                'total_price_with_discount': cart.total_price_with_discount()
            }
        })
    return JsonResponse({
        'success': True,
        'message': f'{product.name} adicionado ao carrinho.',
        'add_discount': False,
        'info_cart_item': {
            'quantity': cart_item.quantity,
            'subtotal': cart_item.subtotal(),
            'discount': cart_item.discount(),
            'percentage_discount': cart_item.percentage_discount(),
            'total_price_with_discount': cart_item.total_price_with_discount()
        },
        'info_cart': {
            'quantity': cart.total_quantity(),
            'total_price': cart.total_price(),
            'total_discount': cart.total_discount(),
            'total_price_with_discount': cart.total_price_with_discount()
        }
    })


@login_required(login_url='users:login', redirect_field_name='next')
def remove_item_to_cart(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Erro no formato dos dados enviados.'})

    productId = data.get('productId')
    quantity = data.get('quantity')

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Quantidade inválida.'})

    if not productId or quantity < 1:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    cart = Cart.objects.get_or_create(user=request.user)[0]

    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(), id=productId)

        if getattr(product, 'stock', None) is None:
            return JsonResponse({'success': False, 'message': 'Erro de cadastro: produto sem estoque vinculado.'})

        '''if product.stock.quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Estoque esgotado.'})'''

        cart_item = get_object_or_404(
            CartItem.objects.select_for_update(),
            cart=cart,
            product=product,
        )

        final_quantity = cart_item.quantity - quantity

        if final_quantity <= 0:
            msg = f'{product.name} foi removido do carrinho removido '
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': msg,
                'remove': True,
                'info_cart': {
                    'quantity': cart.total_quantity(),
                    'total_price': cart.total_price(),
                    'total_discount': cart.total_discount(),
                    'total_price_with_discount': cart.total_price_with_discount()
                }
            })

        cart_item.quantity -= quantity
        cart_item.save()

    if cart_item.discount() > 0:
        return JsonResponse({
            'success': True,
            'message': f'{product.name} foi removido do carrinho.',
            'add_discount': True,
            'info_cart_item': {
                'quantity': cart_item.quantity,
                'subtotal': cart_item.subtotal(),
                'discount': cart_item.discount(),
                'percentage_discount': cart_item.percentage_discount(),
                'total_price_with_discount': cart_item.total_price_with_discount()
            },
            'info_cart': {
                'quantity': cart.total_quantity(),
                'total_price': cart.total_price(),
                'total_discount': cart.total_discount(),
                'total_price_with_discount': cart.total_price_with_discount()
            }
        })

    return JsonResponse({
        'success': True,
        'message': f'{product.name} foi removido do carrinho.',
        'add_discount': False,
        'info_cart_item': {
            'quantity': cart_item.quantity,
            'subtotal': cart_item.subtotal(),
            'discount': cart_item.discount(),
            'percentage_discount': cart_item.percentage_discount(),
            'total_price_with_discount': cart_item.total_price_with_discount()
        },
        'info_cart': {
            'quantity': cart.total_quantity(),
            'total_price': cart.total_price(),
            'total_discount': cart.total_discount(),
            'total_price_with_discount': cart.total_price_with_discount()
        }
    })


@login_required(login_url='users:login', redirect_field_name='next')
def remove_item(request, id):
    if not request.POST:
        raise Http404("No POST data found.")

    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()

    messages.success(
        request, f'{cart_item.product.name} removido do carrinho.')
    return redirect('sale:cart')
