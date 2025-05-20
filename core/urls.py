from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('details/', views.user_details, name='user_details'),
    path('add/', views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admindashboard/', views.admin_dashboard, name='admindashboard'),
    # ✅ Changed route to avoid conflict with Django admin
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),


   path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:user_id>/', views.user_update, name='user_update'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    # urls.py
path("payment-success/", views.payment_success, name="payment-success"),

]
