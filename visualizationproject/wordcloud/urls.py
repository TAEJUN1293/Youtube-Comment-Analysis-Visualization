from django.urls import path
from . import views

urlpatterns = [
    path('trending', views.trending, name='trending'),
    path('trending_detail', views.trending_detail, name='trending_detail')
]