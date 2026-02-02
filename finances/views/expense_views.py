from finances.models import Expense
from finances.forms import ExpenseForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from utils.pagination import make_pagination
from finances.filters import ExpenseFilter
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 10))


@login_required(login_url='users:login', redirect_field_name='next')
def expense_list(request):
    if request.user.is_staff or request.user.is_superuser:
        expense = Expense.objects.all().order_by('-created_at')
    else:
        return redirect('catalog:home')

    form = ExpenseForm()

    expense_filter = ExpenseFilter(request.GET, queryset=expense)

    page_obj, pagination_range = make_pagination(
        request, expense_filter.qs, PER_PAGE)

    status = {
        'total': expense_filter.qs.count(),
        'paid': expense_filter.qs.filter(status='D').count(),
        'pending': expense_filter.qs.filter(status='P').count(),
        'sum_total': expense_filter.qs.aggregate(Sum('amount'))['amount__sum'] or 0,
        'sum_paid': expense_filter.qs.filter(status='D').aggregate(Sum('amount'))['amount__sum'] or 0,
        'sum_pending': expense_filter.qs.filter(status='P').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'finances/pages/expense/expense_list.html', {
        'form': form,
        'status': status,
        'expenses': page_obj,
        'filter': expense_filter,
        'pagination_range': pagination_range,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def register_expense(request):
    if request.method != "POST":
        raise Http404("No POST data found.")

    form = ExpenseForm(request.POST, request.FILES)

    if form.is_valid():
        # save the new user
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Despesa registrada com sucesso!')

    return redirect('finances:expense_list')


@login_required(login_url='users:login', redirect_field_name='next')
def delete_expense(request, expense_id):
    if request.method != "POST":
        raise Http404("No POST data found.")

    expense = get_object_or_404(Expense, id=expense_id)

    expense.delete()
    messages.success(request, 'Despesa excluída com sucesso!')

    return redirect('finances:expense_list')


@login_required(login_url='users:login', redirect_field_name='next')
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)

        if form.is_valid():
            form.save()
            messages.success(request, 'Despesa atualizada com sucesso!')
            return redirect('finances:expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'finances/pages/expense/edit_expense.html', {
        'form': form,
        'expense': expense,
    })
