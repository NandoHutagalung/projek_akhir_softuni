from django.urls import path
from . import views

urlpatterns = [
    path('', views.meja_list, name='meja_list'),
    path('meja/create/', views.meja_create, name='meja_create'),
    path('meja/<int:meja_id>/', views.meja_detail, name='meja_detail'),
    path('meja/<int:meja_id>/delete/', views.meja_delete, name='meja_delete'),
]
