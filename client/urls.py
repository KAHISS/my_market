from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('management/', views.management, name='management'),
    path('add/', views.add_client, name='add_client'),
]
