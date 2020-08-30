from django.urls import path
from api import views

app_name = 'api_v2'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),

    path(
        'user/', views.User.as_view({'get': 'retrieve', 'post': 'create', 'put': 'partial_update'}), name='user_cbv'),

    path('get_all_book/',
         views.GetAllBook.as_view({'get': 'list'}), name='getAllBookCbv'),

    path('favbook/',
         views.FavBook.as_view({'get': 'list', 'post': 'create'}), name='fav_book_cbv'),

    path('braintree_client_token/', views.braintreeClientToken.as_view(
        {'get': 'getClientToken'}), name='braintreeClientToken'),

    path('pay_order/', views.payment.as_view(
        {'get': 'getPayOrderList', 'post': 'createPayOrder'}), name='payOrder'),

    path('pay/', views.payment.as_view(
        {'post': 'createPayment'}), name='pay'),

    path('cart/', views.shopCarManage.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='shopCar'),

    path('chat_check/',
         views.chatCheck.as_view({'get': 'check'}), name='chatCheck'),

    path('book_top3/', views.GetBookTop3.as_view({'get': 'list'}), name='book_top3'),
]
