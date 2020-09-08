from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatRoom.as_view(), name='chat_room'),
]
