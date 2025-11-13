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
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('depot/', views.depot_view, name='depot'),  # Ajouté
    path('retrait/', views.retrait_view, name='retrait'),  # Ajouté
    path('admin/client/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('admin/client/delete/<int:client_id>/', views.delete_client, name='delete_client'),
]