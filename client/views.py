from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, 'client/pages/profile.html')

def management(request):
    return render(request, 'client/pages/clients-management.html')