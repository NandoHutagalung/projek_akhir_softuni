from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:menu_id>/', views.menu_detail, name='menu_detail'),
    path('create/', views.menu_create, name='menu_create'),
    path('<int:menu_id>/edit/', views.menu_edit, name='menu_edit'),
    path('<int:menu_id>/delete/', views.menu_delete, name='menu_delete'),
]
