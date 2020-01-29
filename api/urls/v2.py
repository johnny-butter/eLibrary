from django.urls import path
from api import views

app_name = 'api_v2'

urlpatterns = [
    path('login/', views.login.as_view(), name='login'),

    path(
        'user/', views.getUserList.as_view({'post': 'create'}), name='getUserListCbv'),

    # path('user/<int:pk>/', views.getUserDetail.as_view(
    #     {'get': 'retrieve', 'put': 'update'}), name='getUserDetailCbv'),

    path('user/detail/', views.getUserDetail.as_view(
        {'get': 'retrieve', 'put': 'partial_update'}), name='getUserDetailCbv'),

    path('getallbook/',
         views.getAllBook.as_view({'get': 'list'}), name='getAllBookCbv'),

    path('favbook/',
         views.favBook.as_view({'get': 'list', 'post': 'create'}), name='favBookCbv'),

    path('braintree_client_token/', views.braintreeClientToken.as_view(
        {'get': 'getClientToken'}), name='braintreeClientToken'),

    path('pay_order/', views.payment.as_view(
        {'get': 'getPayOrderList', 'post': 'createPayOrder'}), name='payOrder'),

    path('pay/', views.payment.as_view(
        {'post': 'createTransaction'}), name='pay'),

    path('cart/', views.shopCarManage.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='shopCar'),

    path('chat_check/',
         views.chatCheck.as_view({'get': 'check'}), name='chatCheck'),
]
