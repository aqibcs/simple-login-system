from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('delete-user/', views.delete_user, name='delete-user'),
]
