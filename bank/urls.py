from django.contrib import admin
from django.urls import path
from banking import views

urlpatterns = [
    path('money-bag/', views.money_bag, name='money_bag'),
    path('', views.acceuil, name='acceuil'),
    path('dash-client/', views.dash_client, name='dash_client'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('login-client/', views.login_client, name='login_client'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/client/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('admin/client/delete/<int:client_id>/', views.delete_client, name='delete_client'),

    path('depot/', views.depot_view, name='depot'),
    path('retrait/', views.retrait_view, name='retrait'),

    path('admin/', admin.site.urls),
]
