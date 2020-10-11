from django.urls import path
from api import views

app_name = 'api_v2'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),

    path('user/', views.UserViewSet.as_view(
        {'get': 'retrieve', 'post': 'create', 'put': 'partial_update'}), name='user_cbv'),

    path('get_all_book/', views.GetAllBook.as_view({'get': 'list'}), name='get_all_book_cbv'),

    path('favbook/', views.FavBook.as_view({'get': 'list', 'post': 'create'}), name='fav_book_cbv'),

    path('braintree_client_token/', views.BraintreeClientToken.as_view(
        {'get': 'get_client_token'}), name='braintree_client_token'),

    path('pay_order/', views.Payment.as_view({
        'get': 'get_pay_order_list',
        'post': 'create_pay_order',
        'delete': 'cancel_pay_order',
    }), name='pay_order'),

    path('pay/', views.Payment.as_view({'post': 'create_payment'}), name='pay'),

    path('cart/', views.ShopCarManager.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='shop_car'),

    path('chat_check/', views.ChatCheck.as_view({'get': 'check'}), name='chat_check'),

    path('book_top3/', views.GetBookTop3.as_view({'get': 'list'}), name='book_top3'),
]
