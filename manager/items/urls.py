from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('',views.item_view),
    path('upload/',views.uploadItemsFile)
]
