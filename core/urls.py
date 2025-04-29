from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),


]
