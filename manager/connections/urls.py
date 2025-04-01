from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('',views.connection_view),
    path('generate-code',views.code_view)
]
