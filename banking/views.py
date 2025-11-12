from django.shortcuts import render

# Create your views here.

def money_bag(request):
    return render(request, 'banking/money_bag.html')

def acceuil(request):
    return render(request, 'banking/acceuil.html')

def dash_client(request):
    return render(request, 'banking/dash_client.html')

def login_admin(request):
    return render(request, 'banking/login_admin.html')

def login_client(request):
    return render(request, 'banking/login_client.html')