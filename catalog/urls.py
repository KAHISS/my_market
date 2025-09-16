from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='catalogo'),
    path('product/<int:product_id>/', views.product, name='produtos'),
    path('profile', views.profile, name='perfil'),
    path('cart', views.cart, name='carrinho'),
]
