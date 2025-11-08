from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path('cart/', views.cart_view, name='cart')
]
