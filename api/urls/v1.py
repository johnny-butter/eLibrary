from api.views.v1 import views
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'api_v1'

urlpatterns = [
    url(r'^user/$', views.get_user_list, name='get_user_list'),

    url(r'^user/(?P<pk>[0-9]+)/$',
        views.get_user_detail, name='get_user_detail'),

    url(r'^getallbook/$', views.get_all_book, name='get_all_book'),

    url(r'favbook/$', views.fav_book, name='fav_book'),

    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

    url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
