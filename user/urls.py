from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('register',views.register,name='register'),
    path('home',views.home,name='home'),
    path('edit/<uid>',views.edit,name='edit'),
    path('useredit/<uid>',views.useredit,name='useredit'),
    path('logout',views.user_logout,name='logout'),
    path('delete/<uid>',views.delete,name='delete'),
    path('profile',views.userprofile,name='profile'),
]