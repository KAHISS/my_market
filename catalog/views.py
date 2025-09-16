from django.shortcuts import get_object_or_404, render
from inventory.models import Product

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog/pages/catalogo.html', context={
        'products': products})


def product(request, product_id):
    mock_product_detail = {
        'id': 1,
        'name': f'Produto {1}',
        'price': 299.99,
        'description': 'Esta é uma descrição detalhada de um produto de teste. Serve para que você possa estilizar a página de detalhes sem precisar de dados reais.',
        'cover': {'url': f'https://placehold.co/600x400/9CA3AF/FFF?text=Produto+{product_id}'}
    }
    return render(request, 'catalog/pages/product.html', context={
        'product': mock_product_detail
    })


def profile(request):
    return render(request, 'catalog/pages/client_profile.html')


def cart(request):
    return render(request, 'catalog/pages/cart.html')
