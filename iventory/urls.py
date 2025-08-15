from django.urls import path
from . import views

app_name = 'iventory'

urlpatterns = [
    path('', views.index, name='index'),
]
