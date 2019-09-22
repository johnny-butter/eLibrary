from .. import views
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'api_v1'
urlpatterns = [
    url(r'^user/$', views.getUserList, name='getUserList'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.getUserDetail, name='getUserDetail'),
    url(r'^getallbook/$', views.getAllBook, name='getAllBook'),
    url(r'favbook/$', views.favBook, name='favBook'),
    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
