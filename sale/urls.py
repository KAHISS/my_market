from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:id>/', views.add_item_to_cart, name='cart_add'),
    path('cart/update/<int:id>/', views.update_quantity, name='cart_update'),
    path('cart/remove/<int:id>/', views.remove_item, name='cart_remove'),
]
