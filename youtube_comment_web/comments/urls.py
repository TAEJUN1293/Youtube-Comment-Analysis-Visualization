from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoty_detail', views.detail, name="detail"),
    
]