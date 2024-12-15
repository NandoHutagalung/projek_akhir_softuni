from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('frontend/pesanan', views.add_pesanan, name='frontendpesanan'),
    path('frontend/pesanan/<int:id>', views.list_pesanan, name='listpesananuser'),
    path('frontend/pesanan/edit/<int:pk>', views.edit_pesanan, name='editpesananuser'),
    path('frontend/profileuser/<int:id>', views.profile_update, name='profileuser'),
    path('frontend/pesanan/delete/<int:pk>', views.delete_pesanan, name='deletepesananuser'),
]