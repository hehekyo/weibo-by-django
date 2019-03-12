"""weibo URL Configuration

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
from django.urls import path, include
import xadmin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from users.views import user_login, LoginView, RegisterView, ActivateView, FindbackPwd, ResetPwdView, ModifyPwdView, \
    UserPageView, MainPageLoginView, MyCollectView, HotBlogView, LogoutView
from miniblog.views import MainpageView

urlpatterns = [

                  path('xadmin/', xadmin.site.urls),
                  path('login/', LoginView.as_view(), name="login"),
                  # path('', TemplateView.as_view(template_name="MainPage.html")),
                  path('', MainpageView.as_view(), name='mainpage'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('activate/<str:act_code>', ActivateView.as_view(), name='activate'),
                  path('findbackpwd/', FindbackPwd.as_view(), name='findbackpwd'),
                  path('reset/<str:res_code>', ResetPwdView.as_view(), name="resetpwd"),
                  path('modify/', ModifyPwdView.as_view(), name="modifypwd"),
                  path('captcha/', include('captcha.urls')),

                  # 在主页登录
                  path('mainpagelogin/', MainPageLoginView.as_view(), name='mainpagelogin'),

                  # 用户相关
                  path('user/', include(('users.urls', 'users'), namespace='user')),

                  # 微博主页等
                  path('weibo/', include(('miniblog.urls', 'miniblog'), namespace='weibo')),

                  # 热门微博
                  path('hotblogs/', HotBlogView.as_view(), name="hotblogs"),

                  # 测试路由
                  path('test/', TemplateView.as_view(template_name="LogPage.html")),
                  # （新增）
                  path('index/', MainpageView.as_view(), name='index'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  # operation相关
                  path('operation/', include('operations.urls', namespace='operation')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 配置media的url处理
