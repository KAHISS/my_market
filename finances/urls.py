from django.urls import path
from .views import *

app_name = 'finances'

urlpatterns = [
    path('expenses/', expense_list, name='expense_list'),
    path('expenses/register/', register_expense, name='register_expense'),
    path('expenses/delete/<int:expense_id>/',
         delete_expense, name='delete_expense'),
    path('expenses/edit/<int:expense_id>/',
         edit_expense, name='edit_expense'),
]
