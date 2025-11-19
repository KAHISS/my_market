from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='storage'),
    path('inventory/list', views.product_list, name='product_list'),
]
