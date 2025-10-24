from django.urls import path
from . import views

app_name = 'configs'

urlpatterns = [
    path('', views.home, name='home'),
]
