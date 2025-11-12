"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from banking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('money-bag/', views.money_bag, name='money_bag'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('dash-client/', views.dash_client, name='dash_client'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('login-client/', views.login_client, name='login_client'),
]
