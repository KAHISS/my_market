from django.urls import path
from . import views

app_name = 'provider'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_provider, name='add_provider'),
]
