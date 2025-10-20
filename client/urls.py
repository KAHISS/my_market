from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('profile/<int:id>', views.profile, name='profile'),
    path('', views.management, name='management'),
    path('add/', views.add_client, name='add_client'),
    path('edit/<int:id>/', views.edit_client, name='edit_client'),
    path('delete/<int:id>/', views.delete_client, name='delete_client'),
]
