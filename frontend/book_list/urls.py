from django.urls import path
from . import views

urlpatterns = [
    path('userinfo/', views.user_info_page, name='user_info_page'),

    path('list/', views.book_list, name='book_list'),

    path('favlist/', views.fav_book_list, name='fav_book_list'),
]
