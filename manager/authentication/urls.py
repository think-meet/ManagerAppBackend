from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('reset-password/', views.reset_password_view, name='reset-password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh-access-token/', views.refresh_access_token, name='refresh-access-token')
]