from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('orders/', views.orders, name='orders'),
]
