from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='home'),
    path('search/', views.search, name='search'),
    path('product/<int:product_id>', views.product, name='product'),
    path('category/<int:category_id>', views.category, name='category'),
    path('offers', views.offer, name='offer')
]
