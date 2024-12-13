from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_pesanan, name='list_pesanan'),
    path('add/', views.add_pesanan, name='add_pesanan'),
    path('edit/<int:pk>/', views.edit_pesanan, name='edit_pesanan'),
    path('delete/<int:pk>/', views.delete_pesanan, name='delete_pesanan'),
]
