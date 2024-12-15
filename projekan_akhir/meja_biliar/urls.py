from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='meja_index'),
    path('data', views.meja_list, name='meja_list'),
    path('tambah', views.meja_create, name='meja_create'),
    path('update_status', views.update_status_meja, name='update_status_meja'),
    path('delete/<int:meja_id>', views.meja_delete, name='meja_delete'),
]
