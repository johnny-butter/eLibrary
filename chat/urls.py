from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatRoom.as_view(), name='chatRoom'),
]
