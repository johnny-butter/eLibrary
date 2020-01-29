from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),

    path('register/', views.registerPage, name='registerPage'),
]