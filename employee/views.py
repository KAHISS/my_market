from django.shortcuts import render

# Create your views here.
def pos(request):
    return render(request, 'employee/pages/profile.html')