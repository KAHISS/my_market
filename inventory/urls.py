from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='storage'),
    path('product/<int:id>', views.product, name='product'),
    path('add-product-view', views.addProduct, name='addProductView'),
]
