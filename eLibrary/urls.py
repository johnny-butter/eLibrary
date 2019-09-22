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
from django.conf.urls.i18n import i18n_patterns
from django.utils import translation
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from loginPage import views as loginView
from pay import views as payView
from . import views as elibView

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),

    url(r'^api/v1/', include('api.urls.v1', namespace='v1')),
    url(r'^api/v2/', include('api.urls.v2', namespace='v2')),

    url(r'^elibrary/login/$', loginView.loginPage, name='loginPage'),
    url(r'^elibrary/register/$', loginView.registerPage, name='registerPage'),
    url(r'^elibrary/userinfo/$', elibView.userInfoPage, name='userInfoPage'),
    url(r'^elibrary/booklist/', elibView.bookList, name='booklist'),
    url(r'^elibrary/favbooklist/$', elibView.favBookList, name='favbooklist'),
    url(r'^elibrary/purchase/$', payView.payPage, name='purchasePage'),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
