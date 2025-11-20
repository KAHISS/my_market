from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from sale.models import CartItem, Cart
from inventory.models import Product
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from client.models import Client
from django.shortcuts import redirect
import json


@login_required(login_url='users:login', redirect_field_name='next')
def cart_view(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    clients = Client.objects.all()
    if not cart:
        raise Http404('Cart not found')
    return render(request, 'sale/pages/cart.html', {'cart': cart, 'clients': clients})


@login_required(login_url='users:login', redirect_field_name='next')
def add_item_to_cart(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    data = json.loads(request.body)
    productId = data.get('productId')
    quantity = data.get('quantity')

    if not productId or not quantity:
        return JsonResponse({'success': False, 'message': 'Dados inválidos.'})

    cart = Cart.objects.get_or_create(user=request.user)[0]
    product = get_object_or_404(Product, id=productId)

    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(), id=productId)

        # Verificações de estoque agora são seguras
        if getattr(product, 'stock', None) is None:
            return JsonResponse({'success': False, 'message': 'O produto não tem estoque.'})

        if product.stock.quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Estoque esgotado.'})

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        quantity_add = cart_item.quantity + (1 if quantity == 1 else quantity)
        if quantity_add > product.stock.quantity:
            return JsonResponse({'success': False, 'message': f'Não há estoque suficiente para adicionar mais {quantity}.'})

        cart_item.quantity += quantity

        cart_item.save()
    return JsonResponse({'success': True, 'message': f'{product.name} adicionado ao carrinho.'})


@login_required(login_url='users:login', redirect_field_name='next')
def update_quantity(request, id):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    action = request.POST.get('action')

    with transaction.atomic():
        try:
            cart_item = CartItem.objects.select_for_update().select_related('product__stock').get(
                id=id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            raise Http404("Item não encontrado no seu carrinho.")

        product = cart_item.product
        stock_qty = product.stock.quantity

        match action:
            case 'plus_packaging':
                if (cart_item.quantity + product.unit_per_packaging) <= stock_qty:
                    cart_item.quantity += product.unit_per_packaging
                    cart_item.save()
                else:
                    messages.error(
                        request,
                        f'Não há estoque suficiente para adicionar mais {product.packaging_type.lower()} de "{product.name}".'
                    )

            case 'plus':
                if cart_item.quantity < stock_qty:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.error(
                        request,
                        f'Não há estoque suficiente para adicionar mais "{product.name}".'
                    )

            case 'minus_packaging':
                if cart_item.quantity >= product.unit_per_packaging:
                    cart_item.quantity -= product.unit_per_packaging
                    if cart_item.quantity == 0:
                        cart_item.delete()
                    else:
                        cart_item.save()

            case 'minus':
                if cart_item.quantity > 0:
                    cart_item.quantity -= 1
                    if cart_item.quantity == 0:
                        cart_item.delete()
                    else:
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
