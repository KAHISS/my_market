from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_item_to_cart, name='cart_add'),
    path("cart/remove", views.remove_item_to_cart, name="cart_remove"),
    path('cart/remove/<int:id>/', views.remove_item, name='cart_remove'),
    path('checkout/', views.checkout_cart, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/search/', views.search_order, name='search_order'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order/<int:id>/cancel/', views.order_cancel, name='order_cancel'),
    path('pdv/', views.sale_list, name='sale_list'),
    path('sale/<int:id>/', views.sale_detail, name='sale_detail'),
    path('sale/add/', views.add_item_to_sale, name='sale_add'),
    path('sale/<int:id>/search/', views.sale_search, name='sale_search'),
]
