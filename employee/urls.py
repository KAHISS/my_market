from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('pos/', views.pos, name='pos'),
]
