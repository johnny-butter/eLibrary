from django.urls import path
from . import views

urlpatterns = [
    path('userinfo/', views.userInfoPage, name='userInfoPage'),

    path('list/', views.bookList, name='booklist'),

    path('favlist/', views.favBookList, name='favbooklist'),
]
