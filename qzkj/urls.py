"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from qzkj.views import RegisterView
from qzkj import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    
    # 后台系统admin
    re_path(r'^admin(/)?', admin.site.urls),

    # 网站验证文件
    re_path(r'^MP_verify_yxSL8Vl2Cy7VfcHP.txt', views.verify),
    
    # 注册
    re_path(r'^register/(?P<nickname>.+)/$', views.register),
    re_path(r'^register_submit(/)?$', RegisterView.as_view()),

    # 用户授权相关
    #re_path(r'^user_auth(/)?$', TemplateView.as_view(template_name='user_auth.html'), name='user_auth'),
    re_path(r'^user_auth2', TemplateView.as_view(template_name='user_auth2.html')),
    re_path(r'^get_access_token', views.get_accesstoken), #请求access token


    # 默认主页
    re_path(r'^(/)?$', TemplateView.as_view(template_name='index.html')),


    
]
