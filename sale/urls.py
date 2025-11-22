from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_item_to_cart, name='cart_add'),
    path("cart/remove", views.remove_item_to_cart, name=""),
    path('cart/remove/<int:id>/', views.remove_item, name='cart_remove'),
    path('checkout/', views.checkout_cart, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
]
