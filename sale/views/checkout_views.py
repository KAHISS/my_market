from django.contrib import messages
from django.http import Http404
from django.db import transaction
from sale.models import Cart, Order, OrderItem
from client.models import Client
from inventory.models import Product, Stock
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required(login_url='users:login', redirect_field_name='next')
def checkout_cart(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cart_items.all()

    if not cart_items.exists():
        messages.warning(request, 'Não há itens no carrinho.')
        return redirect('sale:cart')

    try:
        # INÍCIO DA TRANSAÇÃO (Tudo ou Nada)
        with transaction.atomic():

            # 1. Validação de Estoque e Dedução
            for item in cart_items:
                product = item.product
                # CRÍTICO: select_for_update() trava este produto para escrita.
                # Usamos select_related('stock') se o estoque for uma tabela separada (OneToOne)
                # get(id=...) garante que estamos indo no banco buscar a versão mais atual
                stock_db = Stock.objects.select_for_update().get(product=product)

                '''# Verifica se a quantidade pedida é maior que o estoque atual do banco
                if item.quantity > product_db.stock.quantity:
                    # LEVANTA ERRO: Isso força o cancelamento de TUDO que foi feito nesse bloco atomic
                    # inclusive de produtos anteriores do loop que já tinham sido descontados.
                    raise ValueError(
                        f'Não há estoque suficiente para "{product_db.name}".')'''

                # Deduz o estoque
                stock_db.quantity -= item.quantity
                if stock_db.quantity < 0:
                    stock_db.quantity = 0
                stock_db.save()

            # 2. Definição de Cliente/Vendedor
            client = request.user
            seller = None
            payment_method = request.POST.get('payment_method', 'dinheiro')

            if request.user.is_staff or request.user.is_superuser:
                client_id = request.POST.get('client')
                if client_id:
                    # Assume-se que Client tem relação OneToOne com User
                    client = Client.objects.get(id=client_id).user
                    seller = request.user

            # 3. Criação do Pedido
            new_order = Order.objects.create(
                user=client,
                seller=seller,
                status='pendente',
                total_price=cart.total_price(),
                total_discount=cart.total_discount(),
                total_quantity=cart.total_quantity(),
                total_price_with_discount=cart.total_price_with_discount(),
                payment_method=payment_method
            )

            order_items_batch = []

            for item in cart_items:
                order_item = OrderItem(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    subtotal=item.subtotal(),
                    percentage_discount=item.percentage_discount(),
                    discount=item.discount(),
                    total_price_with_discount=item.total_price_with_discount(),
                )
                order_items_batch.append(order_item)

            OrderItem.objects.bulk_create(order_items_batch)

            cart_items.delete()

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('sale:cart')

    messages.success(request, 'Compra realizada com sucesso.')
    return redirect('sale:order_detail', id=new_order.id)
