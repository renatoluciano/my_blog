
from sys import path
from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('add_friend/<int:pk>/', views.add_friend, name='add_friend'),
    path('friendship_list/', views.friendship_list, name='friendship_list'),
    path('remove_friend/<int:pk>/', views.remove_friend, name='remove_friend'),
]