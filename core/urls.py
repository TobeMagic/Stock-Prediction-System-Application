"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

from app.views import *
from userprofile.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),

    path('index', index),
    path('predict/<str:model_name>', predict),
    path('accounts/password/reset/', password_reset, name='account_reset_password'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('userprofile.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media')
]

#  站点标题
admin.site.site_header = ('股票预测系统')  # 变成key 对于其他语言的value
#  标签页标题
admin.site.site_title = ('股票预测系统')
#  页面标题
admin.site.index_title = ('股票预测系统后台')