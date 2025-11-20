from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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
