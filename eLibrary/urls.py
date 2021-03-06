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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings

from frontend.book_list.views import book_list

urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),

    path('', book_list),

    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    url(r'^api/v1/', include('api.urls.v1', namespace='v1')),

    url(r'^api/v2/', include('api.urls.v2', namespace='v2')),

    url(r'^books/', include('frontend.book_list.urls')),

    url(r'^login/', include('frontend.login.urls')),

    url(r'^payment/', include('frontend.pay.urls')),

    path('chat/', include('chat.urls')),

    prefix_default_language=True,
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
