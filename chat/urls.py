from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatRoom.as_view(), name='chatRoom'),
]
