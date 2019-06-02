"""eLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from authApi import views
from authApi import views_cbv
from loginPage import views as loginView
from . import views as elibView
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/user/$', views.getUserList, name='getUserList'),
    url(r'^api/cbv/user/$',
        views_cbv.getUserList.as_view({'post': 'create'}), name='getUserListCbv'),
    url(r'^api/user/(?P<pk>[0-9]+)/$',
        views.getUserDetail, name='getUserDetail'),
    url(r'^api/cbv/user/(?P<pk>[0-9]+)/$', views_cbv.getUserDetail.as_view(
        {'get': 'retrieve', 'put': 'update'}), name='getUserDetailCbv'),
    # url(r'^api/login/', views.api_login, name='api_login'),
    url(r'^api/getallbook/$', views.getAllBook, name='getAllBook'),
    url(r'^api/cbv/getallbook/$',
        views_cbv.getAllBook.as_view({'get': 'list'}), name='getAllBookCbv'),
    url(r'^api/favbook/$', views.favBook, name='favBook'),
    url(r'^api/cbv/favbook/$',
        views_cbv.favBook.as_view({'get': 'list', 'post': 'create'}), name='favBookCbv'),
    # url(r'^api/searchbook$', views.favBook, name='favBook'),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    # url(r'^jwt/refresh-token/', refresh_jwt_token, name='refresh_jwt_token'),
    # url(r'^jwt/api-token-verify/', verify_jwt_token, name='verify_jwt_token'),
    # url(r'^jwt/api-token-auth/', obtain_jwt_token, name='obtain_jwt_token'),
    url(r'^elibrary/login/$', loginView.loginPage, name='loginPage'),
    url(r'^elibrary/register/$', loginView.registerPage, name='registerPage'),
    url(r'^elibrary/userinfo/$', elibView.userInfoPage, name='userInfoPage'),
    url(r'^elibrary/booklist/', elibView.bookList, name='booklist'),
    url(r'^elibrary/favbooklist/$', elibView.favBookList, name='favbooklist'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
