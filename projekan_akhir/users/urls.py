from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:id>/', views.profile_update, name='profile_update'),
    path('create/', views.create_user, name='create_user'),  
    path('', views.user_list, name='user_list'),  
    path('detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
    
]
