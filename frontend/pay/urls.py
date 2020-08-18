from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.payPage, name='purchasePage')
]
