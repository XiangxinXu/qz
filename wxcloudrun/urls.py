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

from wxcloudrun.views import UserView
from wxcloudrun import views
from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    # 计数器接口
    # url(r'^^api/count(/)?$', views.counter),

    re_path(r'^register(/)?$', UserView.as_view()),
    re_path(r'^user_info/(?P<user_n>.+)(/)?$', UserView.as_view()),

    # 获取主页
    re_path(r'^(/)?$', views.index),

    
]
