from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.pay_page, name='pay_page')
]
