from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('profile/', views.profile, name='pos'),
]
