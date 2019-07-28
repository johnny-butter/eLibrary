from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('cbv/', include('authApi.urls_cbv')),

    url(r'^user/$', views.getUserList, name='getUserList'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.getUserDetail, name='getUserDetail'),
    # url(r'^api/login/', views.api_login, name='api_login'),
    url(r'^getallbook/$', views.getAllBook, name='getAllBook'),
    url(r'favbook/$', views.favBook, name='favBook'),
    # url(r'^api/searchbook$', views.favBook, name='favBook'),
    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
