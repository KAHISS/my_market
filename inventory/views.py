from django.shortcuts import render, get_list_or_404
# Create your views here.


def home(request):
    return render(request, 'global/pages/breve.html')
