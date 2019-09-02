from django.urls import path
from . import views_cbv, views_pay

app_name = 'api_v2'
urlpatterns = [
    path(
        'user/', views_cbv.getUserList.as_view({'post': 'create'}), name='getUserListCbv'),

    path('user/<int:pk>/', views_cbv.getUserDetail.as_view(
        {'get': 'retrieve', 'put': 'update'}), name='getUserDetailCbv'),

    path('getallbook/',
         views_cbv.getAllBook.as_view({'get': 'list'}), name='getAllBookCbv'),

    path('favbook/',
         views_cbv.favBook.as_view({'get': 'list', 'post': 'create'}), name='favBookCbv'),

    path('paytoken/', views_pay.brainTreePayment.as_view(
        {'get': 'getClientToken', 'post': 'createPayOrder'}), name='brainTreePayment'),

    path('pay/', views_pay.brainTreePayment.as_view(
        {'post': 'createTransaction'}), name='Pay'),

    path('cart/', views_pay.shopCarManage.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='shopCar'),
]
