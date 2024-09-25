from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('profile/', views.Profile, name='profile'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]
