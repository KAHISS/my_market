from django.urls import path
from . import views

app_name = 'provider'

urlpatterns = [
    path('providers/', views.index, name='index'),
]
