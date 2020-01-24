from django.urls import path
from . import views

urlpatterns = [
    path('userinfo/', views.userInfoPage, name='userInfoPage'),

    path('booklist/', views.bookList, name='booklist'),

    path('favbooklist/', views.favBookList, name='favbooklist'),
]
